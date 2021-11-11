from nixops.deployment import Deployment
from nixops.resources import (
    ResourceDefinition,
    ResourceOptions,
    ResourceState,
    DiffEngineResourceState,
)
from nixops.state import StateDict, RecordId
from nixops_aws.managed_state import ManagedStateDict
from nixops.logger import MachineLogger
import nixops.util
from typing import (
    Annotated,
    Any,
    Dict,
    Generic,
    Iterable,
    Optional,
    Set,
    Tuple,
    Type,
    TypeVar,
    Literal,
    Union,
)
import typing
from .definition import AwsResourceDefinition
from .util import references
from .util.references import ResourceReferenceOption
from .util.eval import transform_options

ConfigT = TypeVar("ConfigT", bound=ResourceOptions)
ManagedResourceStateT = TypeVar("ManagedResourceStateT", bound="AwsManagedResourceState")
T = TypeVar("T")


class AwsResourceState(DiffEngineResourceState, Generic[ConfigT]):
    managed_resources: Dict[
        str, "AwsManagedResourceState"
    ]  # TODO: "AwsManagedResourceState" -> GenericResourceState ?
    _state: StateDict

    def __init__(self, depl: Deployment, name: str, id: RecordId):
        super(DiffEngineResourceState, self).__init__(depl, name, id)
        self._state = StateDict(depl, id)
        self.managed_resources = {}

    def resolve_config(self, defn: AwsResourceDefinition):
        # print("resolve_config", defn.resource_eval, defn.config_type)
        env = dict(self.resolve_references(defn))
        # print("resolve_config env", env)
        return transform_options(defn.resource_eval, defn.config_type, env)

    # def resolve_resource(
    #     self, ref: Optional[str], resource_type, state_type: Type[T]
    # ) -> Optional[T]:

    @staticmethod
    def resolve_resource(depl, ref: Optional[str]) -> Optional["AwsResourceState"]:
        if ref is not None and ref.startswith("res-"):
            ref_path = ref[4:].split(".")

            # TODO: self.depl.get_type_resource(...)
            resource = depl.active_resources.get(ref_path[0], None)
            return resource
        return None

    def resolve_references(self, defn: AwsResourceDefinition):
        for ref in defn.get_references():
            resource = AwsResourceState.resolve_resource(self.depl, ref.value)
            if resource is not None:
                state_path = ref.value[4:].split(".")[2:]
                # print("state_path", state_path)
                if isinstance(resource, AwsResourceState):
                    yield (ref.value, resource._state.get(state_path[0]))
                elif isinstance(resource, DiffEngineResourceState):
                    print("WARNING (OLD DiffEngineResourceState):", type(resource))
                    yield (ref.value, resource._state.get(state_path[0]))
                else:
                    print("WARNING (OLD ResourceState):", type(resource))
                    yield (ref.value, getattr(resource, state_path[0]))

    def _create_managed_resource(
        # self, name: str, type: str, cls: Type["AwsManagedResourceState"], **kwargs
        self, name: str, type: str, cls: Type[ManagedResourceStateT], **kwargs
    ) -> ManagedResourceStateT:
        def _create_state(depl, type, name, id):
            return cls(depl, name, id, **kwargs)  # type: ignore[call-arg]

        # TODO: get rid of this
        with self.depl._db:
            c = self.depl._db.cursor()
            c.execute(
                """create table if not exists ManagedResources(
                     id integer primary key autoincrement,
                     deployment text not null,
                     name text not null,
                     type text not null,
                     foreign key(deployment) references Deployments(uuid) on delete cascade
                   );"""
            )
            c.execute(
                """create table if not exists ManagedResourceAttrs(
                     machine integer not null,
                     name text not null,
                     value text not null,
                     primary key(machine, name),
                     foreign key(machine) references ManagedResources(id) on delete cascade
                   );"""
            )


            # ???
            # c.execute(
            #     """create table if not exists ManagedResourceAttrs(
            #          machine integer not null,
            #          name text not null,
            #          value text not null,
            #          primary key(machine, name),
            #          foreign key(machine) references Resources(id) on delete cascade
            #        );"""

        # TODO: use self.depl._create_resource(name, type)
        #       in the future when managed resources are supported
        with self.depl._db:
            c = self.depl._db.cursor()
            c.execute(
                "select 1 from ManagedResources where deployment = ? and name = ?",
                (self.depl.uuid, name),
            )
            if len(c.fetchall()) != 0:
                raise Exception("resource already exists in database!")
            c.execute(
                "insert into ManagedResources(deployment, name, type) values (?, ?, ?)",
                (self.depl.uuid, name, type),
            )
            id = c.lastrowid
            r = _create_state(self.depl, type, name, id)
            self.managed_resources[name] = r
        return r

    def _delete_managed_resource(self, m: "AwsManagedResourceState") -> None:
        with self.depl._db:
            self.depl._db.execute(
                "delete from ManagedResources where deployment = ? and id = ?",
                (self.depl.uuid, m.id),
            )
        del self.managed_resources[m.name]

    def _check_managed_resources(self):
        # Check all managed resources (synchronize states)
        for resource in self.managed_resources.values():
            resource._check()


ManagedResourceStatus = Union[
    Literal[0],
    Literal[1],
    Literal[2],
    Literal[3],
    Literal[4],
    Literal[5],
    Literal[6],
    Literal[7],
]


# TODO: inherit from ResourceState/GenericResourceState/ImplicitResourceState/ManagedResourceState
class AwsManagedResourceState:
    # TODO merge with ResourceState

    name: str

    UNKNOWN: Literal[0] = 0  # state unknown
    MISSING: Literal[1] = 1  # instance destroyed or not yet created
    STARTING: Literal[2] = 2  # boot initiated
    UP: Literal[3] = 3  # machine is reachable
    STOPPING: Literal[4] = 4  # shutdown initiated
    STOPPED: Literal[5] = 5  # machine is down
    UNREACHABLE: Literal[6] = 6  # machine should be up, but is unreachable
    RESCUE: Literal[7] = 7  # rescue system is active for the machine

    # TODO
    # state: ManagedResourceStatus = nixops.util.attr_property("state", UNKNOWN, int)

    _state: ManagedStateDict

    depl: Deployment
    id: RecordId
    logger: MachineLogger

    def __init__(self, depl: Deployment, name: str, id: RecordId):
        self.depl = depl
        self.name = name
        self.id = id
        self.logger = self.depl.logger.get_logger_for(name)
        self._state = ManagedStateDict(depl, id)
        self.state = self.UNKNOWN  # TODO: we're not storing state (status) in the db for now

    def _check(self):
        return True

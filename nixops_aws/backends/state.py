from nixops.backends import (
    MachineDefinition,
    MachineOptions,
    MachineState,
)
from nixops.resources import (
    ResourceDefinition,
    ResourceOptions,
    ResourceState,
    DiffEngineResourceState,
)
from typing import (
    Annotated,
    Any,
    Generic,
    Iterable,
    Optional,
    Set,
    Tuple,
    Type,
    TypeVar,
)
import typing
from .definition import AwsMachineDefinition
from ..resources.definition import AwsResourceDefinition
from ..resources.state import AwsResourceState
from ..resources.util import references
from ..resources.util.references import ResourceReferenceOption
from ..resources.util.eval import transform_options

ConfigType = TypeVar("ConfigType", bound=MachineOptions)
T = TypeVar("T")


class AwsMachineState(MachineState, Generic[ConfigType]):
    def resolve_config(self, defn: AwsMachineDefinition):
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

    def resolve_references(self, defn: AwsMachineDefinition):
        for ref in defn.get_references():
            resource = AwsMachineState.resolve_resource(self.depl, ref.value)
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

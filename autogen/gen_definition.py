from typing import Any, Set, Dict, Optional, Callable, List, Sequence, Type, ForwardRef
import typing

# TypeVar, Container, Generic
import sys

from resource import Resource

from helpers import uncapitalize, capitalize, pluralize, indent, join_optional
from mypy_boto3_ec2 import type_defs


def gen_dict_constructor(d: Dict[str, str], indentation=3):
    return (
        "{\n"
        + indent(
            "\n".join([f"'{k}': {v}," for (k, v) in sorted(d.items())]),
            indentation=indentation,
        )
        + "\n"
        + indent("}", indentation=indentation - 1)
    )


def gen_dict_arguments(d: Dict[str, str]):
    return indent("\n".join([f"{k}={v}," for (k, v) in sorted(d.items())]))


def gen_boto_call(r: Resource, method: Optional[Callable], typedef, service="ec2"):
    if method is None or typedef is None:
        raise Exception("null method or typedef")

    all_keys = {uncapitalize(k) for k in typedef.__annotations__}
    plural_ids_keys = {r.plural_factory_ids_key, r.plural_ids_key} - {None}
    custom_keys = (
        all_keys
        - plural_ids_keys
        - r.create_keys
        - r.state_keys
        - r.reserved_keys
        - {"DryRun"}
    )
    custom_args = "\n".join([f"# {capitalize(k)}=" for k in custom_keys])

    # d = {
    #     k: f"defn.config.{uncapitalize(k)}"
    #     for k in typedef.__required_keys__
    #     if k not in r.state_keys
    # }
    # TODO
    # {r.plural_managed_ids_key}=[self._state["{r.plural_managed_ids_key}"]]
    # for k in d:
    #     if typedef[k] == Sequence[str]:
    #         d[k] = "[" + d[k] + "]"
    return f"""
self._{method.__name__}(
{indent(custom_args)}
)"""[
        1:
    ]


def gen_resource_imports(r: Resource):
    return f"""
# -*- coding: utf-8 -*-

# Automatic provisioning of {r.plural_resources}.

import boto3
import botocore
import time
from nixops.diff import Handler
import nixops.resources
import nixops.util
from nixops_aws.resources.ec2_common import EC2CommonState
import nixops_aws.ec2_utils
from typing import TYPE_CHECKING, Optional, List, TypedDict, Literal
from . import ec2_common
from .iam_role import IAMRoleState
from ..boto_clients import BotoClients
from .types.{r.snake_case} import {r.camel_case}Options

if TYPE_CHECKING:
    # from mypy_boto3_ec2.literals import {r.factory_camel_case or r.camel_case}StateType
    from mypy_boto3_ec2.type_defs import (
        {r.create_typedef.__name__},
        {r.describe_typedef.__name__},
        {r.modify_typedef.__name__},
        {r.destroy_typedef.__name__},
    )
else:
    # {r.factory_camel_case or r.camel_case}StateType = object
    {r.create_typedef.__name__} = dict
    {r.describe_typedef.__name__} = dict
    {r.modify_typedef.__name__} = dict
    {r.destroy_typedef.__name__} = dict
""".strip()


def gen_resource_definition(r: Resource):
    return f"""
class {r.class_name}Definition(nixops.resources.ResourceDefinition):
    \"\"\"Definition of a {r.resource}.\"\"\"

    config: {r.camel_case}Options

    @classmethod
    def get_type(cls):
        return "{r.kebab_case}"

    @classmethod
    def get_resource_type(cls):
        return "{r.plural_nix_name}"

    def show_type(self):
        return "{{0}}".format(self.get_type())
""".strip()


def gen_resource_handler_declarations(r: Resource):
    physical_keys: Set[str]
    physical_keys = set()

    ignore_keys: Set[str] = set()
    ignore_keys = (
        ignore_keys.union(
            physical_keys,
            {
                r.id_key,
                r.factory_id_key,  # type: ignore[arg-type]
                "additionalInfo",
                "clientToken",
                "context",
                "dryRun",
                "return",
                "tagSpecifications",
            },
        )
        - {None}
    )
    create_only_keys = {"region"}.union(r.create_keys - (r.modify_keys or set()))
    return indent(
        join_optional(
            [
                f"""
self.handle_create_{r.snake_case} = Handler(
    {sorted(create_only_keys - ignore_keys)}, handle=self.realize_create_{r.snake_case}
)""".strip(),
                f"""
self.handle_modify_{r.snake_case} = Handler(
    {sorted((r.modify_keys or set()) - ignore_keys)},
    after=[self.handle_create_{r.snake_case}],
    handle=self.realize_modify_{r.snake_case},
)""".strip()
                if r.modify_keys is not None
                else None,
                f"""
self.handle_tag_update = Handler(
    ["tags"], after=[self.handle_create_{r.snake_case}], handle=self.realize_update_tag
)
""".strip(),
            ],
            separator="\n",
        ),
    )


def gen_resource_state_init(r: Resource):
    return indent(
        f"""
def __init__(self, depl, name, id):
    nixops.resources.DiffEngineResourceState.__init__(self, depl, name, id)
    self._clients = BotoClients()
    # self.{r.factory_snake_case or r.snake_case}_id = self._state.get("{r.factory_id_key or r.id_key}", None)
{gen_resource_handler_declarations(r)}
""".strip()
    )


def gen_resource_ensure_up(r: Resource):
    lhs_id_key: str
    rhs_id_key: str
    plural: bool
    if (
        r.plural_factory_ids_key is not None
        and (
            annotation := r.describe_annotations.get(
                capitalize(r.plural_factory_ids_key)
            )
        )
        is not None
    ):
        if not r.factory_id_key:
            raise Exception("missing factory_id_key")
        lhs_id_key = r.plural_factory_ids_key
        rhs_id_key = r.factory_id_key
    elif (
        r.factory_id_key is not None
        and (annotation := r.describe_annotations.get(capitalize(r.factory_id_key)))
        is not None
    ):
        lhs_id_key = r.factory_id_key
        rhs_id_key = r.factory_id_key
    elif (
        annotation := r.describe_annotations.get(capitalize(r.plural_ids_key))
    ) is not None:
        lhs_id_key = r.plural_ids_key
        rhs_id_key = r.id_key
    elif (annotation := r.describe_annotations.get(capitalize(r.id_key))) is not None:
        lhs_id_key = r.id_key
        rhs_id_key = r.id_key
    elif (
        r.plural_managed_ids_key is not None
        and (
            annotation := r.describe_annotations.get(
                capitalize(r.plural_managed_ids_key)
            )
        )
        is not None
    ):
        if not r.managed_id_key:
            raise Exception("missing managed_id_key")
        lhs_id_key = r.plural_managed_ids_key
        rhs_id_key = r.managed_id_key
    elif (
        r.managed_id_key is not None
        and (annotation := r.describe_annotations.get(capitalize(r.managed_id_key)))
        is not None
    ):
        lhs_id_key = r.managed_id_key
        rhs_id_key = r.managed_id_key
    else:
        print(
            r.plural_factory_ids_key,
            r.factory_id_key,
            r.plural_ids_key,
            r.id_key,
            r.plural_managed_ids_key,
            r.managed_id_key,
            file=sys.stderr,
        )
        print(r.describe_annotations, file=sys.stderr)
        raise Exception("Id key for describe method could not be determined")

    if annotation != Sequence[str]:
        raise Exception("Describe method does not take a list of keys")

    return indent(
        f"""
def ensure_{r.snake_case}_up(self, check):
    defn: {r.class_name}Definition = self.get_defn()
    self._state["region"] = defn.config.region

    if self._state.get("{r.factory_id_key or r.id_key}", None):
        if check:
            try:
                self.get_client("ec2").{r.describe_method.__name__}(
                    {lhs_id_key}=[self._state["{rhs_id_key}"]]
                )
            except botocore.exceptions.ClientError as error:
                errorNotFound = "Invalid{capitalize(rhs_id_key)}.NotFound" # TODO: Check
                if error.response["Error"]["Code"] == errorNotFound:
                    # TODO: recreate?
                    self.warn(
                        "TODO: "
                        "{r.id_key} `{{}}` was deleted from outside nixops,"
                        " recreating ...".format(self._state["{r.factory_id_key or r.id_key}"])
                    )
                    # self.realize_create_{r.snake_case}(allow_recreate = True)
                    # ...
                else:
                    raise error
        if self.state != self.UP:
            self.wait_for_{r.factory_snake_case or r.snake_case}_available()
""".strip()
    )


def gen_resource_wait_for_available(r: Resource):
    return indent(
        f"""
def wait_for_{r.factory_snake_case or r.snake_case}_available(self):
    def check_response_field(name, value, expected_value):
        if value != expected_value:
            raise Exception(
                "Unexpected value ‘{{0}} = {{1}}’ in response, expected ‘{{0}} = {{2}}’".format(
                    name, value, expected_value
                )
            )
    self.state = self.UNKNOWN
    while self.state != self.UP:
{indent("response = " + gen_boto_call(r, r.describe_method, r.describe_typedef), indentation=2)}
        for config in response["{r.factory_camel_case or r.camel_case}Configs"]:
            check_response_field(
                "{r.factory_camel_case or r.camel_case}Id",
                config["{r.factory_camel_case or r.camel_case}Id"],
                self._state["{r.factory_id_key or r.id_key}"],
            )
            self.state = self.resource_state_from_boto(config["{r.factory_camel_case or r.camel_case}State"])
        if self.state not in {{self.UP, self.STARTING}}:
            raise Exception(
                "{r.factory_resource or r.resource} {{0}} is in an unexpected state {{1}}".format(
                    self._state["{r.factory_id_key or r.id_key}"], config["{r.factory_camel_case or r.camel_case}State"]
                )
            )
        # if len(response["{r.plural_camel_case}"]) == 1:
        #     {r.snake_case} = response["{r.plural_camel_case}"][0]
        # else:
        #     raise Exception(
        #         "couldn't find {r.factory_resource} `{{}}`, please run deploy with --check".format(
        #             {r.id_key}
        #         )
        #     )
        self.log_continue(".")
        time.sleep(1)
    self.log_end("done")

    with self.depl._db:
        self.state = self.UP
""".strip()
    )


def gen_resource_realize_create(r: Resource):
    if r.implicit:
        return ""
    return indent(
        f"""
def realize_create_{r.snake_case}(self, allow_recreate):
    defn: {r.class_name}Definition = self.get_defn()
    if self.state == self.UP:
        if not allow_recreate:
            raise Exception(
                "{r.factory_resource} `{{}}` definition changed and it needs to be recreated"
                " use --allow-recreate if you want to create a new one".format(
                    self._state['{r.factory_id_key or r.id_key}']
                )
            )
        self.warn("{r.resource} definition changed, recreating...")
        self._destroy()

    self._state["region"] = defn.config.region

    vpc_id = defn.config.vpcId

    if vpc_id.startswith("res-"):
        res = self.depl.get_typed_resource(
            vpc_id[4:].split(".")[0], "vpc", VPCState
        )
        vpc_id = res._state["vpcId"]

    zone = defn.config.zone if defn.config.zone else ""
    self.log("creating {r.factory_resource or r.resource} in context `{{0}}`".format(vpc_id))
{indent(gen_boto_call(r, r.create_method, r.create_typedef), indentation=1)}
    # self._state['{r.factory_id_key or r.id_key}'] = response[TODO]["{r.factory_id_key or r.id_key}"]
    # self.zone = {r.snake_case}["AvailabilityZone"]

    with self.depl._db:
        self.state = self.STARTING
        # self._state["zone"] = self.zone
        # self._state["region"] = defn.config.region

    def tag_updater(tags):
        self.get_client("ec2").create_tags(
            Resources=[self._state["{r.factory_id_key or r.id_key}"]],
            Tags=[{{"Key": k, "Value": tags[k]}} for k in tags],
        )

    self.update_tags_using(tag_updater, user_tags=defn.config.tags, check=True)

    self.wait_for_{r.factory_snake_case or r.snake_case}_available()
""".strip()
    )


def gen_resource_realize_modify(r: Resource):
    if r.implicit:
        return ""
    return indent(
        f"""
def realize_modify_{r.snake_case}(self, allow_recreate):
    defn: {r.class_name}Definition = self.get_defn()

    self.log("modifying {r.factory_resource or r.resource} `{{0}}` in context `{{1}}`".format(self._state['{r.factory_id_key or r.id_key}'], ""))
{indent(gen_boto_call(r, r.modify_method, r.modify_typedef), indentation=1)}

    self.wait_for_{r.factory_snake_case or r.snake_case}_available()

    # with self.depl._db:
    #     self._state["policy"] = defn.config.policy
    #     self._state["routeTableIds"] = new_rtbs
""".strip()
    )


def gen_resource_realize_update_tag(r: Resource):
    return indent(
        f"""
def realize_update_tag(self, allow_recreate):
    defn: {r.class_name}Definition = self.get_defn()
    tags = {{k: v for k, v in defn.config.tags.items()}}
    tags.update(self.get_common_tags())
    self.get_client("ec2").create_tags(
        Resources=[self._state["{r.factory_id_key or r.id_key}"]],
        Tags=[{{"Key": k, "Value": tags[k]}} for k in tags],
    )
""".strip()
    )


def gen_resource_state_from_boto(r: Resource):
    return indent(
        """
def resource_state_from_boto(self, state: BatchStateType) -> int:
    if state == "active":
        return self.UP
    elif state == "cancelled":
        return self.MISSING
    else:
        # TODO
        return self.UNKNOWN
""".strip()
    )


def gen_resource_destroy(r: Resource):
    return indent(
        f"""
def _destroy(self):
    if self.state not in {{self.UP, self.STARTING}}:
        return
    self.log("deleting {r.factory_resource or r.resource} `{{0}}`".format(self._state['{r.factory_id_key or r.id_key}']))
    try:
        self._retry(lambda:
{indent(gen_boto_call(r, r.destroy_method, r.destroy_typedef), indentation=3)}
        )
    except botocore.exceptions.ClientError as error:
        if error.response["Error"]["Code"] == "InvalidSubnetID.NotFound":
            self.warn("{r.factory_id_key} `{{}}` was already deleted".format(self._state['{r.factory_id_key or r.id_key}']))
        else:
            raise error

    with self.depl._db:
        self.state = self.MISSING
        self._state["{r.factory_id_key or r.id_key}"] = None
        # self._state["{{r.managed_id_keys}}"] = None
        # self._state["region"] = None
        # self._state["zone"] = None
""".strip()
    )


def gen_boto_optional_args(
    r: Resource,
    typedef,
    service="ec2",
):
    if typedef is None:
        raise Exception("null typedef")

    optional_keys = {uncapitalize(k) for k in typedef.__optional_keys__} - {"dryRun"}
    optional_config_keys = optional_keys.intersection(r.create_keys)
    optional_state_keys = optional_keys.intersection(r.state_keys)
    optional_args = {
        **{capitalize(k): f"defn.config.{k}" for k in optional_config_keys},
        **{capitalize(k): f"self._state['{k}']" for k in optional_state_keys},
    }
    return "\n".join(
        [
            "optional_args: Dict[str, Any] = dict()",
            *[
                f"""
if {optional_args[k]} is not None:
    optional_args['{k}'] = {optional_args[k]}
""".strip()
                for k in sorted(optional_args.keys())
            ],
        ]
    )


def gen_boto_unpack_args(
    r: Resource,
    typedef,
    service="ec2",
):
    if typedef is None:
        raise Exception("null typedef")

    def extract_forwardref(
        t: Type, namespace: dict = type_defs.__dict__
    ) -> Optional[Type]:
        non_none_args = [
            arg_type for arg_type in typing.get_args(t) if arg_type is not type(None)
        ]
        if isinstance(t, ForwardRef):
            return t._evaluate(namespace, {}, set())
        elif len(non_none_args) == 1:
            inner_type = non_none_args[0]
            if isinstance(inner_type, ForwardRef):
                return inner_type._evaluate(namespace, {}, set())
        else:
            return None

    forwardrefs = {k: extract_forwardref(t) for k, t in typedef.__annotations__.items()}
    forwardrefs = {k: t for k, t in forwardrefs.items() if t is not None}
    return "\n".join(
        [
            f"def unpack_{typedef.__name__}(config: {typedef}.__name__) -> {typedef}:",
            *[
                indent(
                    "\n".join(
                        [
                            f"""if config.{uncapitalize(k)} is not None:""",
                            *[
                                "\n".join(
                                    [
                                        indent(
                                            f"""if defn.config.{uncapitalize(k)}.{uncapitalize(fk)} is not None:"""
                                        ),
                                        indent(
                                            f"""extra_args['{k}']['{fk}'] = defn.config.{uncapitalize(k)}.{uncapitalize(fk)}""",
                                            indentation=2,
                                        ),
                                    ]
                                )
                                for fk in sorted(forwardrefs[k].__annotations__.keys())
                            ],
                        ]
                    )
                )
                for k in sorted(forwardrefs.keys())
            ],
        ]
    )


def gen_boto_complex_args(
    r: Resource,
    typedef,
    service="ec2",
):
    if typedef is None:
        raise Exception("null typedef")

    # def extract_forwardref(t: Type, namespace: dict = type_defs.__dict__) -> Optional[Type]:
    #     non_none_args = [
    #         arg_type for arg_type in typing.get_args(t) if arg_type is not type(None)
    #     ]
    #     if isinstance(t, ForwardRef):
    #         return t._evaluate(namespace, {}, set())
    #     elif len(non_none_args) == 1:
    #         inner_type = non_none_args[0]
    #         if isinstance(inner_type, ForwardRef):
    #             return inner_type._evaluate(namespace, {}, set())
    #     else:
    #         return None

    # forwardrefs = {k: extract_forwardref(t) for k, t in typedef.__annotations__.items()}
    # forwardrefs = {k: t for k, t in forwardrefs.items() if t is not None}
    # return "\n".join(
    #     [
    #         "# TODO: replace extra_args",
    #         "extra_args: Dict[str, Any] = dict()",
    #         *[
    #             "\n".join(
    #                 [
    #                     f"""if defn.config.{uncapitalize(k)} is not None:""",
    #                     *[
    #                         "\n".join(
    #                             [
    #                                 indent(
    #                                     f"""if defn.config.{uncapitalize(k)}.{uncapitalize(fk)} is not None:"""
    #                                 ),
    #                                 indent(
    #                                     f"""extra_args['{k}']['{fk}'] = defn.config.{uncapitalize(k)}.{uncapitalize(fk)}""",
    #                                     indentation=2,
    #                                 ),
    #                             ]
    #                         )
    #                         for fk in sorted(forwardrefs[k].__annotations__.keys())
    #                     ],
    #                 ]
    #             )
    #             for k in sorted(forwardrefs.keys())
    #         ],
    #     ]
    # )
    return gen_boto_unpack_args(r, typedef, service)


def gen_boto_wrapper(
    r: Resource,
    method: Optional[Callable],
    annotations: Optional[Dict[str, Any]],
    typedef,
    service="ec2",
):
    if method is None or annotations is None or typedef is None:
        if r.implicit:
            return
        else:
            raise Exception("null method, annotations, or typedef")

    required_keys = {uncapitalize(k) for k in typedef.__required_keys__}
    required_plural_keys = required_keys.intersection(
        {r.plural_factory_ids_key, r.plural_ids_key, r.plural_managed_ids_key}
    )
    required_config_keys = required_keys.intersection(r.create_keys)
    required_state_keys = required_keys.intersection(r.state_keys)
    # required_plural_state_keys: Set[(str, str)]
    required_plural_state_keys = required_plural_keys.intersection(
        {pluralize(k) for k in r.state_keys}
    )
    required_args = {
        **{capitalize(k): f"defn.config.{k}" for k in required_config_keys},
        **{capitalize(k): f"self._state['{k}']" for k in required_state_keys},
        **{
            capitalize(k): f"[self._state['{k[:-1]}']]"
            for k in required_plural_state_keys
        },
    }
    return indent(
        f"""
def _{method.__name__}(
    self, **kwargs
):
    defn: {r.class_name}Definition = self.get_defn()
{indent(gen_boto_optional_args(r, typedef), indentation=1)}
{indent(gen_boto_complex_args(r, typedef), indentation=1)}
    response = self.get_client("ec2").{method.__name__}(
{indent(gen_dict_arguments(required_args), indentation=1)}
        **optional_args,
        **kwargs,
    )

    # if not kwargs.get("DryRun"):
    #     with self.depl._db:
    #         self.state = self.UP

    #         # Save response to deployment state
    #         self.{r.factory_id_key or r.id_key} = response["{r.factory_camel_case or r.camel_case}Id"]

    #         # Save request to deployment state
    #         self._save_config_data(request["{r.factory_camel_case or r.camel_case}Config"])

    return response
""".strip()
    )


def gen_resource_state(r: Resource):
    location_attr_name = "zone" if "zone" in r.create_keys else "region"
    return f"""
class {r.class_name}State(nixops.resources.DiffEngineResourceState, EC2CommonState):
    \"\"\"State of a {r.resource}.\"\"\"

    definition_type = {r.class_name}Definition

    _clients: BotoClients

    state = nixops.util.attr_property(
        "state", nixops.resources.ResourceState.MISSING, int
    )
    access_key_id = nixops.util.attr_property("accessKeyId", None)
    _reserved_keys = EC2CommonState.COMMON_EC2_RESERVED + {sorted(r.reserved_keys)}

    def get_client(self, service: Literal["ec2", "iam"]):
        client = self._clients.get(service)
        if client:
            return client

        new_access_key_id = (
            self.get_defn().config.accessKeyId if self.depl.definitions else None  # type: ignore
        ) or nixops_aws.ec2_utils.get_access_key_id()
        if new_access_key_id is not None:
            self.access_key_id = new_access_key_id
        if self.access_key_id is None:
            raise Exception(
                "please set 'accessKeyId', $EC2_ACCESS_KEY or $AWS_ACCESS_KEY_ID"
            )
        (access_key_id, secret_access_key) = nixops_aws.ec2_utils.fetch_aws_secret_key(
            self.access_key_id
        )
        region: str = self._state["region"]
        client = boto3.session.Session().client(
            service_name=service,
            region_name=region,
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key,
        )
        self._clients[service] = client
        return client

{gen_resource_state_init(r)}

    @classmethod
    def get_type(cls):
        return "{r.kebab_case}"

    def show_type(self):
        s = super({r.class_name}State, self).show_type()
        {location_attr_name} = self._state.get("{location_attr_name}")
        if {location_attr_name} is not None:
            s = "{{0}} [{{1}}]".format(s, {location_attr_name})
        return s

    @property
    def resource_id(self):
        return self._state['{r.factory_id_key or r.id_key}']

    def prefix_definition(self, attr):
        return {{("resources", "{r.plural_nix_name}"): attr}}

    def get_physical_spec(self):
        return {gen_dict_constructor(r.physical_spec)}

    def get_definition_prefix(self):
        return "resources.{r.plural_nix_name}."

    def create_after(self, resources, defn):
        # return {{r for r in resources if isinstance(r, TODO)}}
        return {{}}

    def create(
        self,
        defn: {r.class_name}Definition,
        check: bool,
        allow_reboot: bool,
        allow_recreate: bool,
    ):
        nixops.resources.DiffEngineResourceState.create(
            self, defn, check, allow_reboot, allow_recreate
        )
        self.ensure_{r.snake_case}_up(check)

{gen_resource_destroy(r)}

    def destroy(self, wipe=False):
        self._destroy()
        return True

    # Synchronize state changes

{gen_resource_wait_for_available(r)}

{gen_resource_ensure_up(r)}

    # Realize state changes

{gen_resource_realize_create(r)}

{gen_resource_realize_modify(r)}

{gen_resource_realize_update_tag(r)}

    # Marshalling

{gen_resource_state_from_boto(r)}

    # Boto wrappers

{gen_boto_wrapper(r, r.create_method, r.create_annotations, r.create_typedef)}

{gen_boto_wrapper(r, r.describe_method, r.describe_annotations, r.describe_typedef)}

{gen_boto_wrapper(r, r.modify_method, r.modify_annotations, r.modify_typedef)}

{gen_boto_wrapper(r, r.destroy_method, r.destroy_annotations, r.destroy_typedef)}

""".strip()

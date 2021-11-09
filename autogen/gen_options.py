import collections
from datetime import datetime
from helpers import uncapitalize, capitalize, pluralize, indent, join_optional
import re
from resource import Resource
import sys
from typing import (
    Any,
    Callable,
    Dict,
    ForwardRef,
    List,
    Literal,
    Optional,
    Sequence,
    Set,
    Type,
    Union,
    get_args,
    get_origin,
)
from mypy_boto3_ec2 import type_defs


def gather_forwardrefs(
    r: Resource, t: Type, namespace: dict = type_defs.__dict__
) -> Dict[str, Type]:
    forwardrefs: Dict[str, Type] = {
        **{
            t.__forward_arg__: t._evaluate(namespace, {}, set())
            for k, t in t.__annotations__.items()
            if isinstance(t, ForwardRef)
        },
        **{
            get_args(t)[0]
            .__forward_arg__: get_args(t)[0]
            ._evaluate(namespace, {}, set())
            for k, t in t.__annotations__.items()
            if (hasattr(t, "__args__") and isinstance(get_args(t)[0], ForwardRef))
        },
    }
    gathered_types = [
        {k: ref_type, **gather_forwardrefs(r, ref_type, namespace)}
        for k, ref_type in forwardrefs.items()
    ]
    return {k: t for ds in gathered_types for k, t in ds.items()}


def gen_options_imports(r: Resource):
    typedefs = gather_forwardrefs(r, r.create_typedef)
    imported_dicts = ",".join(sorted(typedefs.keys()))
    untyped_dicts = "\n".join([f"{k} = dict" for k in sorted(typedefs.keys())])
    return f"""
from typing import Mapping, Sequence, Optional, Union, Any, Literal
from nixops.resources import ResourceOptions

if TYPE_CHECKING:
    from mypy_boto3_ec2.type_defs import (
        {imported_dicts},
        {r.create_typedef.__name__},
        {r.modify_typedef.__name__},
    )
else:
{indent(untyped_dicts)}
    {r.create_typedef.__name__} = dict
    {r.modify_typedef.__name__} = dict
""".strip()


def render_type(
    t: Type, field_name: Optional[str] = None, namespace: dict = type_defs.__dict__
):
    if field_name == "instanceType":
        return "str"
    elif isinstance(t, ForwardRef):
        return re.sub(
            "(Request)*TypeDef$",
            "Options",
            t._evaluate(namespace, {}, set()).__name__,
        )
    elif hasattr(t, "__args__"):
        type_args = [render_type(arg_type) for arg_type in get_args(t)]
        origin = get_origin(t)
        if (origin is list) or (origin is Sequence) or (origin is collections.Sequence):
            return f"Sequence[{','.join(type_args)}]"
        elif origin is Literal:
            return f"Literal{type_args}"
        elif origin is Optional or type(None) in get_args(t):
            return f"Optional[{','.join(type_args)}]"
        elif origin is Union:
            return f"Union[{','.join(type_args)}]"
        else:
            raise Exception("Unknown type", t, get_origin(t))
    elif t is str:
        return "str"
    elif t is int:
        return "int"
    elif t is float:
        return "float"
    elif t is bool:
        return "bool"
    elif t is datetime:
        return "datetime"
    else:
        return str(t)


def gen_options_type_fields(r: Resource, t: Type, namespace: dict = type_defs.__dict__):
    required_keys = {uncapitalize(k) for k in t.__required_keys__}
    optional_keys = {uncapitalize(k) for k in t.__optional_keys__}

    fields_types = {uncapitalize(k): t for k, t in t.__annotations__.items()}
    fields_rendered = {k: render_type(t, k) for k, t in fields_types.items()}

    return "\n".join(
        [
            *[f"{k}: {fields_rendered[k]}" for k in sorted(list(required_keys))],
            *[
                f"{k}: Optional[{fields_rendered[k]}]"
                for k in sorted(list(optional_keys))
            ],
        ]
    )


def gen_options_type_fields(r: Resource, t: Type, namespace: dict = type_defs.__dict__):
    required_keys = {uncapitalize(k) for k in t.__required_keys__}
    optional_keys = {uncapitalize(k) for k in t.__optional_keys__}

    fields_types = {uncapitalize(k): t for k, t in t.__annotations__.items()}
    fields_rendered = {k: render_type(t, k) for k, t in fields_types.items()}

    return "\n".join(
        [
            *[f"{k}: {fields_rendered[k]}" for k in sorted(list(required_keys))],
            *[
                f"{k}: Optional[{fields_rendered[k]}]"
                for k in sorted(list(optional_keys))
            ],
        ]
    )


def gen_options_forwardref_types(
    r: Resource, t: Type, namespace: dict = type_defs.__dict__
) -> List[str]:
    forwardrefs = {
        **{
            uncapitalize(k): t._evaluate(namespace, {}, set())
            for k, t in t.__annotations__.items()
            if isinstance(t, ForwardRef)
        },
        **{
            uncapitalize(k): get_args(t)[0]._evaluate(namespace, {}, set())
            for k, t in t.__annotations__.items()
            if (hasattr(t, "__args__") and isinstance(get_args(t)[0], ForwardRef))
        },
    }
    return [
        "\n\n\n".join([gen_options_type(r, t), gen_options_unpack(r, t, t)])
        for k, t in sorted(forwardrefs.items())
    ]


def gen_options_type(r: Resource, t: Type, class_name: Optional[str] = None) -> str:
    if class_name is None:
        class_name = re.sub("(Request)*TypeDef$", "", t.__name__)

    return (
        "\n\n".join(gen_options_forwardref_types(r, t))
        + "\n\n"
        + "\n".join(
            [
                f"class {class_name}Options(ResourceOptions):",
                indent(gen_options_type_fields(r, t)),
            ]
        )
    )


def gen_options_unpack(
    r: Resource,
    source_type: Type,
    dest_type: Type,
    class_name: Optional[str] = None,
    unpack_name: Optional[str] = None,
    namespace: dict = type_defs.__dict__,
) -> str:
    if class_name is None:
        class_name = re.sub("(Request)*TypeDef$", "", dest_type.__name__)

    def render_unpack_simple(t: Type, field_name: str, kwfields_name: str = "kwargs"):
        origin = get_origin(t)
        # arg_types = list(set(get_args(t)) - {type(None)})
        if origin in {list, Sequence, collections.Sequence}:
            return f"list(config.{uncapitalize(field_name)}) if config.{uncapitalize(field_name)} else None"
        # elif origin is Union and type(None) in get_args(t):
        #     return f"if config.{uncapitalize(field_name)}: {render_unpack_simple(arg_type, field_name)}"
        else:
            return f"""config.{uncapitalize(field_name)}"""

    def render_unpack_typedef(t: Type, rendered_field_name: str, overrides: str):
        class_name = re.sub(
            "(Request)*TypeDef$", "", t._evaluate(namespace, {}, set()).__name__
        )
        class_camel_case = re.sub("([A-Z])", "_\\1", class_name)[1:].lower()
        return f"unpack_{class_camel_case}({rendered_field_name}, **{overrides})"

    def render_unpack_sequence_typedef(t: Type, field_name: str):
        return f"[{render_unpack_typedef(t, 'c', 'overrides')} for c, overrides in zip(config.{uncapitalize(field_name)}, kwargs.get('{field_name}', repeat({{}})))]"

    def render_unpack_wrapped_typedef(t: Type, field_name: str):
        origin = get_origin(t)
        arg_types = get_args(t)
        if isinstance(t, ForwardRef):
            return render_unpack_typedef(
                t,
                "config." + uncapitalize(field_name),
                f"kwargs.get('{field_name}', {{}})",
            )
        elif origin in {list, Sequence, collections.Sequence}:
            return render_unpack_sequence_typedef(arg_types[0], field_name)

    def render_unpack_assignment(t: Type, field_name: str):
        origin = get_origin(t)
        arg_types = get_args(t)
        is_forwardref = isinstance(t, ForwardRef) or (
            origin
            in {
                list,
                Sequence,
                collections.Sequence,
            }
            and isinstance(arg_types[0], ForwardRef)
        )
        if is_forwardref:
            return f"""{field_name} = {render_unpack_wrapped_typedef(t, field_name)} if config.{uncapitalize(field_name)} else kwargs.get('{field_name}')"""
        else:
            return f"""{field_name} = kwargs.get('{field_name}', {render_unpack_simple(t, field_name)})"""

    def render_dict_assignment(t: Type, field_name: str):
        return f"""if {field_name} is not None: r['{field_name}'] = {field_name}"""

    def render_unpack_argument(t: Type, field_name: str):
        # return f"""{field_name} = kwargs.get('{field_name}', {render_unpack_simple(t, field_name)})"""
        return render_unpack_assignment(t, field_name)

    class_camel_case = re.sub("([A-Z])", "_\\1", class_name)[1:].lower()
    unpack_name = unpack_name or class_camel_case
    source_keys = {k for k in source_type.__annotations__}
    optional_source_keys = set(dest_type.__optional_keys__).intersection(source_keys)
    required_source_keys = set(dest_type.__required_keys__).intersection(source_keys)
    extra_arg_keys = set(dest_type.__required_keys__) - source_keys
    extra_arg_types_rendered = [
        f"{k}: {render_type(dest_type.__annotations__[k], k)}"
        for k in sorted(extra_arg_keys)
    ]
    extra_arg_assign_rendered = [f"{k} = {k}" for k in sorted(extra_arg_keys)]
    return "\n".join(
        [
            f"""
def unpack_{unpack_name}(
    config: {class_name}Options,
    {"".join([s + ', ' for s in extra_arg_types_rendered])}
    **kwargs,
) -> {dest_type.__name__}:
""".strip(),
            f"""    r = {dest_type.__name__}("""
            + ",".join(
                [
                    *extra_arg_assign_rendered,
                    *[
                        render_unpack_argument(dest_type.__annotations__[k], k)
                        for k in sorted(required_source_keys)
                    ],
                ]
            )
            + ")",
            indent(
                "\n".join(
                    [
                        "\n".join(
                            [
                                render_unpack_assignment(
                                    dest_type.__annotations__[k], k
                                ),
                                render_dict_assignment(dest_type.__annotations__[k], k),
                            ]
                        )
                        for k in sorted(optional_source_keys)
                    ],
                )
            ),
            # f"""    return {dest_type.__name__}(r)""",
            f"""    return r""",
        ]
    )


def gen_options_types(r: Resource):
    assert r.create_typedef is not None
    related_types = "\n\n".join(gen_options_forwardref_types(r, r.create_typedef))
    return f"""
{related_types}


class {r.class_name}Options(ResourceOptions):
    # {r.factory_id_key or r.id_key}: str
{indent(gen_options_type_fields(r, r.create_typedef))}

    # Common EC2 auth options
    accessKeyId: str
    region: str

    # Common EC2 options
    tags: Mapping[str, str]

{gen_options_unpack(r, r.create_typedef, r.create_typedef, r.class_name, unpack_name='create_' + (r.factory_snake_case or r.snake_case))}
{gen_options_unpack(r, r.create_typedef, r.modify_typedef, r.class_name, unpack_name='modify_' + (r.factory_snake_case or r.snake_case))}
""".strip()

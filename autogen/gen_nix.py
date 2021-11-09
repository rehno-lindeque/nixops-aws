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


def gen_nix_type_fields(r: Resource, t: Type, nix_name: Optional[str], namespace: dict = type_defs.__dict__):
    required_keys = {uncapitalize(k) for k in t.__required_keys__}
    optional_keys = {uncapitalize(k) for k in t.__optional_keys__}

    def render_type(t: Type, field_name: Optional[str] = None):
        origin = get_origin(t)
        non_none_args = [
            arg_type for arg_type in get_args(t) if arg_type is not type(None)
        ]
        non_none_arg_origins = {get_origin(arg) for arg in non_none_args}
        is_simple_arg = non_none_arg_origins == {None} and not any(
            [isinstance(arg_type, ForwardRef) for arg_type in non_none_args]
        )

        rendered_args = " ".join([render_type(arg_type, field_name) for arg_type in non_none_args])
        if field_name == "instanceType":
            return "types.str"
        elif isinstance(t, ForwardRef):
            return "types.submodule " + uncapitalize(
                re.sub(
                    "(Request)*TypeDef$",
                    "Options",
                    t._evaluate(namespace, {}, set()).__name__,
                )
            )
        elif hasattr(t, "__args__"):
            if origin in {list, Sequence, collections.Sequence}:
                if is_simple_arg:
                    return f"types.listOf {rendered_args}"
                else:
                    return f"types.listOf ({rendered_args})"
            elif origin is Literal:
                arg_strs = ['"' + arg + '"' for arg in sorted(list(non_none_args))]
                return f"types.enum [{' '.join(arg_strs)}]"
            elif origin is Optional or type(None) in get_args(t):
                if is_simple_arg:
                    return f"types.nullOr {rendered_args}"
                else:
                    return f"types.nullOr ({rendered_args})"
            elif origin is Union:
                return f"Union[{rendered_args}]"
            else:
                raise Exception("Unknown type", t, get_origin(t))
        elif t is str:
            ref = r.cross_references.get((nix_name, field_name))
            if ref is not None:
                return f"types.either types.str (resource \"{ref[0]}\")"
            else:
                return "types.str"
        elif t is int:
            return "types.int"
        elif t is float:
            return "types.float"
        elif t is bool:
            return "types.bool"
        elif t is datetime:
            return "types.str"
        else:
            return str(t)

    def render_example(t: Type, field_name: str):
        origin = get_origin(t)
        non_none_args = [
            arg_type for arg_type in get_args(t) if arg_type is not type(None)
        ]
        if origin in {list, Sequence, collections.Sequence}:
            return """
example = [
    # Undocumented
];
""".strip()
        elif origin is Optional or type(None) in get_args(t):
            return render_example(non_none_args[0], field_name)
        else:
            return """# example = ;"""

    def render_default(t: Type, field_name: str):
        origin = get_origin(t)
        non_none_args = [
            arg_type for arg_type in get_args(t) if arg_type is not type(None)
        ]
        non_none_arg_origins = {get_origin(arg) for arg in non_none_args}
        if origin in {list, Sequence, collections.Sequence}:
            return """# default = [];""".strip()
        elif origin is Optional or type(None) in get_args(t):
            if isinstance(non_none_args[0], ForwardRef):
                return """default = {};"""
            elif non_none_arg_origins.intersection(
                {list, Sequence, collections.Sequence}
            ):
                return """default = [];"""
            elif Literal in non_none_arg_origins:
                return """# default = "";"""
            else:
                return """default = null;"""
        else:
            return """# default = ;"""

    def render_option(t: Type, field_name: str):
        return f"""
mkOption {{
{indent(render_default(t, field_name))}
{indent(render_example(t, field_name))}
    type = {render_type(t, field_name)};
    description = ''
    Undocumented
    '';
}};""".strip()

    fields_types = {uncapitalize(k): t for k, t in t.__annotations__.items()}
    for k in sorted(list(optional_keys)):
        fields_types[k] = Optional[fields_types[k]]
    fields_rendered = {k: render_option(t, k) for k, t in fields_types.items()}

    return "\n".join(
        [
            *[f"{k} = {fields_rendered[k]}" for k in sorted(list(required_keys))],
            *[f"{k} = {fields_rendered[k]}" for k in sorted(list(optional_keys))],
        ]
    )


def gen_nix_forwardref_types(
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
    return [gen_nix_type(r, t) for k, t in sorted(forwardrefs.items())]


def gen_nix_type(r: Resource, t: Type, nix_name: Optional[str] = None) -> str:
    if nix_name is None:
        nix_name = re.sub("(Request)*TypeDef$", "", t.__name__)

    return (
        "\n\n".join(gen_nix_forwardref_types(r, t))
        + "\n"
        + indent(
            "\n".join(
                [
                    f"{uncapitalize(nix_name)}Options = {{",
                    indent("options = {"),
                    indent(gen_nix_type_fields(r, t, nix_name), indentation=2),
                    indent("};"),
                    "};",
                ]
            )
        )
    )


def gen_nix_types(r: Resource):
    assert r.create_typedef is not None
    related_types = "\n\n".join(gen_nix_forwardref_types(r, r.create_typedef))
    return f"""
let
  cfg = config.{r.nix_name};
  {related_types}
in
{{
  imports = [ ./common-ec2-auth-options.nix ];

  options = {{
    {r.factory_id_key or r.id_key} = mkOption {{
      default = "";
      type = types.str;
      description = ''
        {r.factory_resource or r.resource} ID (set by NixOps)
      '';
    }};
{indent(gen_nix_type_fields(r, r.create_typedef, None), indentation=2)}
  }}
  // (import ./common-ec2-options.nix {{ inherit lib; }});

  config = {{
    _type = "aws-{r.kebab_case}";
  }};
}}
""".strip()

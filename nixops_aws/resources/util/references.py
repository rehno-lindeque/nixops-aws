import inspect
from nixops.resources import ResourceOptions
from nixops.util import ImmutableValidatedObject
from typing import (
    Annotated,
    Any,
    Callable,
    Generic,
    Iterable,
    Mapping,
    NewType,
    Optional,
    Sequence,
    Tuple,
    Type,
    TypeVar,
    Union,
)
import typing

T = TypeVar("T")
ValueType = TypeVar("ValueType")
ReferenceType = TypeVar("ReferenceType")
Unresolved = NewType("Unresolved", object)

# # TODO: ResourceOptionReference could be implemented as NewType["ResourceOptionReference", T].
# #       However, this would require serialization in from the nix type to the python NewType.
# #       For now Annotated maintains backward compatibility with str.
# ResourceReferenceOption = Annotated[Union[T, str], "ResourceReferenceOption"]


class ResourceReferenceOption(
    ImmutableValidatedObject, Generic[ReferenceType, ValueType]
):
    value: Union[Unresolved, ValueType]
    reference: Optional[ReferenceType]

    def __init__(self, unresolved: Union[ReferenceType, ValueType]):
        super(ResourceReferenceOption, self).__init__(value=Unresolved(unresolved))

    @classmethod
    def resolved(cls, value: ValueType, reference: Optional[ReferenceType]):
        return super(ResourceReferenceOption, cls.__new__(cls)).__init__(
            value=value, reference=reference
        )


def is_reference_type(t: Type) -> bool:
    """
    Test if a type is ResourceReferenceOption type. Note that this checks against a type not a value.
    """
    # # TODO: If ResourceReferenceOption is a NewType, this could be implemented at the value level.
    # #       (I.e. isinstance(value, ResourceReferenceOption))
    # return typing.get_origin(t) is Annotated and typing.get_args(t)[1:2] == ("ResourceReferenceOption",)  # type: ignore[attr-defined]
    return typing.get_origin(t) is ResourceReferenceOption


def collect(value) -> Iterable[ResourceReferenceOption]:
    """
    Recurse iterables to find all ResourceReferenceOption instances.
    """
    if isinstance(value, ResourceReferenceOption):
        yield value
    elif isinstance(value, ResourceOptions) or isinstance(value, tuple) or isinstance(value, dict):
        for val in value:
            yield from collect(val)


def collect_options_instances(value) -> Iterable[ResourceOptions]:
    """
    Recurse iterables to find all ResourceOptions instances.
    """
    if isinstance(value, ResourceOptions):
        yield value
    if isinstance(value, Iterable):
        for val in value:
            if isinstance(val, ResourceOptions):
                yield val


def collect_types(
    t: Type,
) -> Iterable[Type[ResourceReferenceOption]]:
    if is_reference_type(t):
        yield t
    else:
        for type_arg in typing.get_args(t):
            yield from collect_types(type_arg)

    # Assume compatibility if source type and destintation type shares Mapping base


# class Context:
#     key: str
#     remainder: dict
# def collect_dict(d, context: List[Context]=[]) -> KeyValStream[ResourceReferenceOption]:
#     result = dict()
#     for k,v in d.items():
#         if isinstance(v, ResourceReferenceOption)
#             result[k] = ResourceReferenceOption.resolve(v)
#         elif isinstance(v, dict):
#             result[k] = collect_dict(v, [*context, Context(key=k, remainder=result)])


# def collect(
#     config, config_type
# ) -> Iterable[Tuple[T, Type[ResourceReferenceOption[str,T]]]]:
#     """
#     Collect all reference values along with type information about the reference types.
#     """
#     for resource_options in collect_options_instances(config):
#         for k, t in typing.get_type_hints(
#             resource_options, include_extras=True
#         ).items():
#             val = getattr(config, k)

#             if val is None or isinstance(val, ResourceOptions):
#                 continue

#             if is_reference_type(t):
#                 yield (val, t)
#                 continue

#             # Handle Unions with ResourceReferenceOption
#             type_origin = typing.get_origin(t)
#             type_args = tuple(set(typing.get_args(t)) - {type(None)})
#             if (
#                 type_origin is Union
#                 and len(type_args) == 1
#                 and is_reference_type(type_args[0])
#             ):
#                 # Allow Optional[ResourceReferenceOption]
#                 yield (val, type_args[0])
#             else:
#                 # Disallow complex datastructures containing references
#                 # TODO: Complex datastructures (arbitrary Union and Iterable types) could be supported if ReferenceOptionType can be serialized into a NewType in future.
#                 if any(True for _ in collect_types(t)):
#                     raise Exception(
#                         "Bug: ‘{0}.{1}’ is too complex for reference resolution.\nAvoid embedding ResourceReferenceOption in ‘{2}’.".format(
#                             type(resource_options).__name__, k, type_origin
#                         )
#                     )

# ObjType = TypeVar(ImmutableValidatedObject, bound=ImmutableValidatedObject)
# SourceT = TypeVar("SourceT")
# DestT = TypeVar("DestT")
# MkConstructor: Callable[[Type[SourceT], Type[DestT]], Callable[[SourceT], DestT]]

# ClassT = TypeVar("ClassT", bound=type)


# def _type_dispatch(Type[T], f: Callable[Type[T], Callable]):
#     t_origin = ...
#     if inspect.isclass(t):
#         return f(t)
#     elif t_origin is Union:
#         functions = tuple(
#             c
#             for c in (_mk_constructor(source_t, t) for t in typing.get_args(t_origin))
#             if c is not None
#         )
#         if len(functions) > 1:
#             raise Exception(
#                 "Bug: Multiple known conversions between source type ‘{0}’ and destination type ‘{1}’".format(
#                     source_t, dest_t
#                 )
#         else:
#             return functions[0]

# def _transform_value(
#     source_type: Type[SourceT], dest_type: Type[DestT]
#     f: Callable[[DestT], DestT],
# ) -> Optional[Callable[[SourceT], DestT]]:

#     # NOTE: SourceT is assumed to be a class, not a special form.
#     #       However, we don't (can't?) currently enforce this via the MkConstructor type signature.

#     source_t = typing.get_args(source_type)[0]
#     source_origin = typing.get_origin(source_t) or source_t
#     dest_t = typing.get_args(dest_type)[0]
#     dest_origin = typing.get_origin(dest_t) or dest_t

#     if inspect.isclass(dest_origin):
#         # Pass through identical types
#         if source_t is dest_t:
#             return lambda value: value

#         if inspect.isclass(source_origin):
#             # Pass through direct subclasses without modification
#             # NOTE: Type arguments are not allowed in the destination type because this could
#             #       invalidate the subclass check.
#             if issubclass(source_origin, dest_origin) and typing.get_args(dest_t) == ():
#                 return lambda value: value

#             # Assume that all Sequence types can be initialized from a generator (Iterable)
#             if issubclass(dest_origin, Sequence):
#                 return lambda value: dest_t(v for v in value)

#             # Assume that all subclasses of ImmutableValidatedObject can be constructed from named arguments
#             # Assume that all subclasses of Mapping can be constructed from named arguments
#             # (Destination class does not need to subclass Mapping)
#             if issubclass(source_origin, Mapping) and (
#                 issubclass(dest_origin, Mapping)
#                 or issubclass(dest_origin, ImmutableValidatedObject)
#             ):
#                 return lambda value: dest_origin(**value)

#     # Lift SourceT to Union[SourceT,...] as needed
#     if dest_origin is Union:
#         constructors = tuple(
#             c
#             for c in (_mk_constructor(source_t, t) for t in typing.get_args(dest_t))
#             if c is not None
#         )
#         if len(constructors) > 1:
#             raise Exception(
#                 "Bug: Multiple known conversions between source type ‘{0}’ and destination type ‘{1}’".format(
#                     source_t, dest_t
#                 )
#             )
#         # elif source_t in set(dest_args):
#         #     return lambda value: _mk_constructor(value, dest[0]) if

#     # raise Exception("Bug: No known conversion between source type ‘{0}’ and destination type ‘{1}’".format(source_t, dest_t))
#     return None


# def parent(env: dict):
#     def _mk_resolver(
#         source_type: Type[SourceT], dest_type: Type[DestT]
#     ) -> Optional[Callable[[SourceT], DestT]]:
#         dest_t = typing.get_args(dest_type)[0]
#         dest_origin = typing.get_origin(dest_t) or dest_t
#         if inspect.isclass(dest_origin) and issubclass(dest_origin, ResourceReferenceOption):
#             return lambda value: ResourceReferenceOption.resolve(value, env)
#         else:
#             return _mk_constructor(source_type, dest_type)

# def _transform_value(
#     value: Any, target_type: Type[T], instantiate_to_type: Callable[[Any, T], T]
# ) -> T:
#     def is_immutable_validated_object_type(t: Type) -> bool:
#         return inspect.isclass(t) and issubclass(t, ImmutableValidatedObject)

#     t = typing.get_args(target_type)[0]  # type: ignore[attr-defined]

#     # Untyped, pass through
#     if t is Any:
#         return value

#     targs = tuple(set(typing.get_args(t)) - {type(None)})  # type: ignore[attr-defined]
#     torigin = typing.get_origin(t) or t  # type: ignore[attr-defined]

#     # Support ImmutableValidatedObject, or any subclass (including subclasses that take type arguments).
#     if is_immutable_validated_object_type(torigin):
#         if isinstance(value, Mapping):
#             value = torigin(**value)
#         else:
#             value = torigin(value)
#     elif len(targs) == 1 and is_immutable_validated_object_type(targs[0]):

#         # Support Optional[ImmutableValidatedObject]
#         if torigin is Union:
#             if value is not None:
#                 value = _transform_value(value, targs[0])

#         # Support Sequence[ImmutableValidatedObject]
#         elif (
#             isinstance(value, Sequence)
#             and inspect.isclass(torigin)
#             and issubclass(tuple, torigin)
#         ):
#             value = tuple(_transform_value(v, targs[0]) for v in value)

#     typeguard.check_type(key, value, t)

#     return value


# def resolve(obj: ObjType, env: dict) -> ObjType:
#     # annotations = typing.get_type_hints(obj, include_extras=False)

#     # for k, v in obj:
#     #     if key == "_frozen":
#     #         continue
#     #     default = getattr(self, key) if hasattr(self, key) else None
#     #     value = kw.get(key, default)
#     #     setattr(self, key, _transform_value(value, anno.get(key)))
#     pass

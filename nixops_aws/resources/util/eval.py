# -*- coding: utf-8 -*-
import inspect
from nixops.resources import ResourceEval, ResourceOptions
from typing import (
    Annotated,
    Any,
    Callable,
    Dict,
    Iterable,
    List,
    Mapping,
    NewType,
    Optional,
    Sequence,
    Set,
    TYPE_CHECKING,
    Tuple,
    Type,
    TypeVar,
    Union,
)
import typing
from .references import ResourceReferenceOption

SourceT = TypeVar("SourceT")
DestT = TypeVar("DestT")

# def _mk_constructor(
#     source_type: Type[SourceT], dest_type: Type[DestT]
# ) -> Optional[Callable[[SourceT], DestT]]:
#     """
#     Make a constructor that takes source type as input and produces destination type as output.

#     Returns None if the conversion is not possible.
#     """

#     (source_t,) = typing.get_args(source_type)
#     (dest_t,) = typing.get_args(dest_type)

#     # TODO: can this be enforced at the type level?
#     if not (typing.get_args(source_t) == () and typing.get_args(dest_t) == ()):
#         raise Exception("Bug: Subscripted generics cannot be used with mk_constructor")
#     if not inspect.isclass(source_t):
#         raise Exception("Bug: mk_constructor expects a class for the source type")
#     if isinstance(dest_t, typing._SpecialForm):
#         raise Exception("Bug: Special form types cannot be used with mk_constructor")

#     # Pass through source type if it subclasses the destination type
#     if issubclass(source_t, dest_t):
#         return lambda value: _assert_cast(value, source_t)

#     # Convert source type to destination type using the destination type's constructor
#     if inspect.isclass(dest_t):
#         if issubclass(dest_t, ImmutableValidatedObject):
#             # Assume ImmutableValidatedObject subclass takes named arguments if the value is a Mapping
#             if issubclass(source_t, Mapping):
#                 return lambda value: dest_t(**_assert_cast(value, Mapping))

#             # Assume ImmutableValidatedObject has a compatible single argument constructor
#             return lambda value: dest_t(_assert_cast(value, source_t))

#         # Assume source and destination have compatible constructors if they share the Mapping base class
#         if issubclass(source_t, Mapping) and issubclass(dest_t, Mapping):
#             return lambda value: dest_t(_assert_cast(value, Mapping))

#         # Assume source and destination have compatible constructors if they share the Sequence base class
#         if issubclass(source_t, Sequence) and issubclass(dest_t, Sequence):
#             return lambda value: dest_t(_assert_cast(value, source_t))

#     # Source and destination types are not compatible
#     return None


# _MkConstructor = Callable[
#     [Type[SourceT], Type[DestT]],
#     Optional[Callable[[SourceT], DestT]],
# ]

# def _copy_construct(
#     value: Any, dest_type: Type[DestT], mk_constructor: _MkConstructor[SourceT, DestT] = _mk_constructor,
# ) -> DestT:
#     source_t = type(value)
#     (dest_t,) = typing.get_args(dest_type)

#     def _dispatch_union(union_type_args):
#         constructors = tuple(
#             c
#             for c in (
#                 mk_constructor(source_t, typing.get_origin(t) or t)
#                 for t in union_type_args
#             )
#             if c is not None
#         )
#         if len(constructors) > 1:
#             raise Exception(
#                 "Bug: Multiple known conversions between source type ‘{0}’ and destination type ‘{1}’".format(
#                     source_t, dest_t
#                 )
#             )
#         return constructors[0] if len(constructors) == 1 else None

#     dest_origin = typing.get_origin(dest_t) or dest_t
#     constructor = (
#         _dispatch_union(typing.get_args(dest_t))
#         if dest_origin is Union
#         else mk_constructor(source_t, dest_origin)
#     )

#     if constructor is None:
#         raise Exception(
#             "Bug: No known conversions between source type ‘{0}’ and destination type ‘{1}’".format(
#                 source_t, dest_t
#             )
#         )

#     return constructor(value)


def transform_options(
    resource_eval: ResourceEval, dest_type: Type[DestT], environment: Optional[dict]
):
    annotations = typing.get_type_hints(dest_type, include_extras=True)

    # def _dispatch_union(union_type_args):
    #     constructors = tuple(
    #         c
    #         for c in (
    #             mk_constructor(source_t, typing.get_origin(t) or t)
    #             for t in union_type_args
    #         )
    #         if c is not None
    #     )
    #     if len(constructors) > 1:
    #         raise Exception(
    #             "Bug: Multiple known conversions between source type ‘{0}’ and destination type ‘{1}’".format(
    #                 source_t, dest_t
    #             )
    #         )
    #     return constructors[0] if len(constructors) == 1 else None

    # (dest_t,) = typing.get_args(dest_type)
    dest_t = dest_type
    dest_class = typing.get_origin(dest_t) or dest_t

    def _transform_value(value, annotation):
        # Transform child ResourceEval
        if isinstance(value, ResourceEval):
            if inspect.isclass(annotation) and issubclass(annotation, ResourceOptions):
                # print("resource options", value)
                return transform_options(value, annotation, environment)
            else:
                return value

        # Transform to reference type
        if inspect.isclass(annotation) and issubclass(
            annotation, ResourceReferenceOption
        ):
            # if environment is not None:
            #     print("reference option", value, environment.get(value))
            # Return unresolved if no environment is supplied
            if environment is None:
                return ResourceReferenceOption(value)
            # Resolve reference
            reference = value
            resolved = environment.get(value)
            if resolved is not None:
                return ResourceReferenceOption.resolved(value=resolved, reference=reference)
            # Value was not a reference (TODO: improve resolved check - currently we just assume no resolution means its a value)
            return ResourceReferenceOption.resolved(value=value, reference=None)

        # Pass through simple types
        return value

    def _simplify(annotation):
        type_origin = typing.get_origin(annotation)
        # Simplify Optional
        while type_origin is Union:
            type_args = tuple(
                arg for arg in typing.get_args(annotation) if arg is not type(None)
            )  # noqa: E721
            if len(type_args) != 1:
                type_origin = None
            else:
                annotation = type_args[0]
                type_origin = typing.get_origin(annotation)
        return (annotation, type_origin)

    def _transform_each():
        for k, anno in annotations.items():
            if k == "_frozen":
                continue
            value = resource_eval.get(k)
            anno, anno_origin = _simplify(anno)
            if inspect.isclass(anno_origin) and issubclass(anno_origin, Sequence):
                elem_anno, elem_origin = _simplify(typing.get_args(anno)[0])
                yield (
                    k,
                    tuple(
                        _transform_value(elem_value, elem_origin or elem_anno)
                        for elem_value in value
                    )
                )
            # elif anno_origin is Mapping:
            #     elem_anno, elem_origin = _simplify(typing.get_args(anno))
            #     yield (
            #         k,
            #         _transform_value(
            #             dict(
            #                 _transform_value(elem_value, elem_anno or elem_origin)
            #                 for elem_key, elem_value in value.items()
            #             )
            #         ),
            #     )
            else:
                yield (k, _transform_value(value, anno_origin or anno))

    # print("dest_class", dest_class)
    # print("resource_eval", resource_eval)
    # print("transformed", dict(_transform_each()))

    return dest_class(**dict(_transform_each()))

    # constructor = (
    #     _dispatch_union(typing.get_args(dest_t))
    #     if dest_origin is Union
    #     else mk_constructor(source_t, dest_origin)
    # )

    # if constructor is None:
    #     raise Exception(
    #         "Bug: No known conversions between source type ‘{0}’ and destination type ‘{1}’".format(
    #             source_t, dest_t
    #         )
    #     )

    # return constructor(value)

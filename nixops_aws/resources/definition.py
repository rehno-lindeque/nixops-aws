from nixops.resources import ResourceDefinition, ResourceOptions
from typing import Annotated, Any, Iterable, Set, Tuple, Type, TypeVar, Generic
import typing
from .util import references
from .util.references import ResourceReferenceOption
from .util.eval import transform_options

ConfigT = TypeVar("ConfigT", bound=ResourceOptions)


class AwsResourceDefinition(ResourceDefinition, Generic[ConfigT]):
    """Base class for Aws resource definitions."""

    config: ConfigT
    config_type: Type[ConfigT]

    def prepare_config(self, config_type) -> ConfigT:
        return transform_options(self.resource_eval, config_type, None)

    def get_references(self) -> set:
        """
        Get all state references.
        """
        # return set(ref for ref, _ in references.collect(self.config))
        return set(references.collect(self.config))

    def show_type(self) -> str:
        """A short description of the type of resource this is"""
        return self.get_type()


# TODO: inherit from ResourceDefinition/GenericResourceDefinition/ImplicitResourceDefinition/ManagedResourceDefinition
class AwsManagedResourceDefinition:
    pass

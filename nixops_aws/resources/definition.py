from nixops.resources import ResourceDefinition, ResourceOptions
from typing import Annotated, Any, Iterable, Set, Tuple, Type, TypeVar, Generic
import typing
from .util import references
from .util.references import ResourceReferenceOption
from .util.eval import transform_options

ConfigType = TypeVar("ConfigType", bound=ResourceOptions)


class AwsResourceDefinition(ResourceDefinition, Generic[ConfigType]):
    """Base class for Aws resource definitions."""

    config: ConfigType
    config_type: Type[ConfigType]

    def prepare_config(self, config_type) -> ConfigType:
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

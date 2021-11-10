from nixops.backends import MachineDefinition, MachineState, MachineOptions
from typing import Annotated, Any, Iterable, Set, Tuple, Type, TypeVar, Generic
import typing
from ..resources.util import references
from ..resources.util.references import ResourceReferenceOption
from ..resources.util.eval import transform_options

ConfigType = TypeVar("ConfigType", bound=MachineOptions)


class AwsMachineDefinition(MachineDefinition, Generic[ConfigType]):
    """Base class for Aws machine definitions."""

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

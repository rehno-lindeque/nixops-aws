from nixops.backends import MachineDefinition, MachineState, MachineOptions
from typing import Annotated, Any, Iterable, Set, Tuple, Type, TypeVar, Generic
import typing
from ..resources.util import references
from ..resources.util.references import ResourceReferenceOption
from ..resources.util.eval import transform_options

ConfigT = TypeVar("ConfigT", bound=MachineOptions)


class AwsMachineDefinition(MachineDefinition, Generic[ConfigT]):
    """Base class for Aws machine definitions."""

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

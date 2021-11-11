from dataclasses import dataclass, field
from helpers import uncapitalize, capitalize, pluralize
from typing import Any, Set, Dict, Optional, Callable, List, Sequence, Type, Tuple

# TODO:
# Higher-kinded data could potentially be used to fix ignore[assignment] issues
# if/when HKT is added to to the typing package.
# See https://github.com/python/typing/issues/548


@dataclass
class Resource:
    # class_name: str
    # snake_case: str
    # factory_resource_id_name: str   # request / reservation / etc
    # concrete_resource_id_name: str  # instance / subnet / group / etc
    # physical_spec: Set[str]

    # Mandatory fields
    resource: str  # E.g. "spot fleet" or "instance"
    create_method: Callable
    describe_method: Callable

    # Optional fields
    # (methods)
    factory_resource: Optional[str] = None  # E.g. "spot fleet request"
    managed_resource: Optional[str] = None  # E.g. "instance"
    modify_method: Optional[Callable] = None
    destroy_method: Optional[Callable] = None
    # (typedefs)
    create_typedef: Optional[Type] = None
    describe_typedef: Optional[Type] = None
    modify_typedef: Optional[Type] = None
    destroy_typedef: Optional[Type] = None

    # Automatic fields
    # (annotations)
    create_annotations: Dict[str, Any] = None  # type: ignore[assignment]
    describe_annotations: Dict[str, Any] = None  # type: ignore[assignment]
    modify_annotations: Optional[Dict[str, Any]] = None
    destroy_annotations: Optional[Dict[str, Any]] = None
    # (formatting)
    snake_case: str = None  # type: ignore[assignment]
    kebab_case: str = None  # type: ignore[assignment]
    camel_case: str = None  # type: ignore[assignment]
    factory_snake_case: Optional[str] = None
    factory_camel_case: Optional[str] = None
    managed_camel_case: Optional[str] = None
    # (specifics)
    class_name: str = None  # type: ignore[assignment]
    nix_name: str = None  # type: ignore[assignment]
    # (keys)
    id_key: str = None  # type: ignore[assignment]
    factory_id_key: Optional[str] = None
    managed_id_key: Optional[str] = None
    create_keys: Set[str] = None  # type: ignore[assignment]
    describe_keys: Set[str] = None  # type: ignore[assignment]
    modify_keys: Optional[Set[str]] = None
    destroy_keys: Optional[Set[str]] = None
    reserved_keys: Set[str] = None  # type: ignore[assignment]
    state_keys: Set[str] = None  # type: ignore[assignment]
    # (pluralized)
    plural_resources: str = None  # type: ignore[assignment]
    plural_snake_case: str = None  # type: ignore[assignment]
    plural_camel_case: str = None  # type: ignore[assignment]
    plural_nix_name: str = None  # type: ignore[assignment]
    plural_ids_key: str = None  # type: ignore[assignment]
    plural_factory_ids_key: Optional[str] = None
    plural_managed_ids_key: Optional[str] = None
    plural_factory_resources: Optional[str] = None
    plural_factory_snake_case: Optional[str] = None
    # plural_classes: Optional[str] = None
    # (human readable)
    # resource: Optional[str] = None
    # human_resource_name: Optional[str] = None
    # resource_in_context: Optional[str] = None # E.g. "subnet in vpc"
    # (complex)
    physical_spec: Dict[str, str] = None  # type: ignore[assignment]
    cross_references: Dict[Tuple[str], Tuple[str]] = field(default_factory=dict)
    implicit: bool = False

    def __post_init__(self):
        # (annotations)
        if self.create_annotations is None:
            self.create_annotations = {
                k: v
                for k, v in self.create_method.__annotations__.items()
                if k != "return"
            }
        if self.describe_annotations is None:
            self.describe_annotations = {
                k: v
                for k, v in self.describe_method.__annotations__.items()
                if k != "return"
            }
        if self.modify_annotations is None and self.modify_method is not None:
            self.modify_annotations = {
                k: v
                for k, v in self.modify_method.__annotations__.items()
                if k != "return"
            }
        if self.destroy_annotations is None and self.destroy_method is not None:
            self.destroy_annotations = {
                k: v
                for k, v in self.destroy_method.__annotations__.items()
                if k != "return"
            }

        # (formatting)
        if self.snake_case is None:
            self.snake_case = self.resource.replace(" ", "_")
        if self.kebab_case is None:
            self.kebab_case = self.resource.replace(" ", "-")
        if self.camel_case is None:
            self.camel_case = "".join(
                [capitalize(piece) for piece in self.resource.split(" ")]
            )
        if self.factory_resource is not None and self.factory_snake_case is None:
            self.factory_snake_case = self.factory_resource.replace(" ", "_")
        if self.factory_resource is not None and self.factory_camel_case is None:
            self.factory_camel_case = "".join(
                [capitalize(piece) for piece in self.factory_resource.split(" ")]
            )
        if self.managed_resource is not None and self.managed_camel_case is None:
            self.managed_camel_case = "".join(
                [capitalize(piece) for piece in self.managed_resource.split(" ")]
            )

        # (specifics)
        if self.class_name is None:
            self.class_name = f"Aws{self.camel_case}"
        if self.nix_name is None:
            # self.nix_name = uncapitalize(self.camel_case)
            self.nix_name = f"aws{self.camel_case}"

        # (keys)
        if self.id_key is None:
            self.id_key = f"{uncapitalize(self.camel_case)}Id"
        if self.factory_camel_case is not None and self.factory_id_key is None:
            self.factory_id_key = f"{uncapitalize(self.factory_camel_case)}Id"
        if self.managed_camel_case is not None and self.managed_id_key is None:
            self.managed_id_key = f"{uncapitalize(self.managed_camel_case)}Id"
        if self.create_keys is None:
            self.create_keys = {uncapitalize(k) for k in self.create_annotations}
        if self.describe_keys is None:
            self.describe_keys = {
                k[0].lower() + k[1:] for k in self.describe_annotations or set()
            }
        if self.modify_annotations is not None and self.modify_keys is None:
            self.modify_keys = {k[0].lower() + k[1:] for k in self.modify_annotations}
        if self.destroy_annotations is not None and self.destroy_keys is None:
            self.destroy_keys = {k[0].lower() + k[1:] for k in self.destroy_annotations}
        if self.reserved_keys is None:
            self.reserved_keys = {self.id_key, self.factory_id_key} - {None}
        if self.state_keys is None:
            # self.state_keys = {self.id_key, self.factory_id_key} - {None}
            self.state_keys = {"region", self.factory_id_key or self.id_key}

        # (pluralized)
        if self.plural_resources is None:
            self.plural_resources = pluralize(self.resource)
        if self.plural_snake_case is None:
            self.plural_snake_case = pluralize(self.snake_case)
        if self.plural_camel_case is None:
            self.plural_camel_case = pluralize(self.camel_case)
        if self.plural_nix_name is None:
            self.plural_nix_name = pluralize(self.nix_name)
        if self.plural_ids_key is None:
            self.plural_ids_key = pluralize(self.id_key)
        if self.factory_id_key is not None and self.plural_factory_ids_key is None:
            self.plural_factory_ids_key = pluralize(self.factory_id_key)
        if self.managed_id_key is not None and self.plural_managed_ids_key is None:
            self.plural_managed_ids_key = pluralize(self.managed_id_key)
        if self.factory_resource is not None and self.plural_factory_resources is None:
            self.plural_factory_resources = pluralize(self.factory_resource)
        if (
            self.factory_snake_case is not None
            and self.plural_factory_snake_case is None
        ):
            self.plural_factory_snake_case = pluralize(self.factory_snake_case)

        # (human readable)
        # if self.resource is None:
        #     self.resource = "TODO"
        # if self.human_resource_name is None:
        #     self.human_resource_name = "TODO"
        # if self.human_concrete_resource_name_in_context is None:
        #     self.human_concrete_resource_name_in_context = (
        #         "TODO"  # e.g. subnet in vpc `...`
        #     )

        # (complex)
        if self.physical_spec is None:
            self.physical_spec = dict()
            self.physical_spec[
                self.factory_id_key or self.id_key
            ] = f"self._state['{self.factory_id_key or self.id_key}']"


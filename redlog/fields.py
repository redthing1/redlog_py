"""
Field system for structured logging.
"""

from dataclasses import dataclass
from typing import Any, List

from .utils import stringify


@dataclass
class Field:
    """Simple structured field for key-value logging.

    Stores a key and value as strings - no complex lazy evaluation.
    """

    key: str
    value: str

    def __init__(self, key: str, value: Any) -> None:
        self.key = key
        self.value = stringify(value)


class FieldSet:
    """Collection of fields with simple operations.

    Optimized for the common case of small numbers of fields.
    """

    def __init__(self, fields: List[Field] = None) -> None:
        self._fields = fields or []

    def add(self, field: Field) -> None:
        """Add a field to this field set."""
        self._fields.append(field)

    def merge(self, other: "FieldSet") -> None:
        """Merge another field set into this one."""
        self._fields.extend(other._fields)

    def with_field(self, field: Field) -> "FieldSet":
        """Return a new field set with an additional field (immutable operation)."""
        return FieldSet(self._fields + [field])

    def with_fields(self, other: "FieldSet") -> "FieldSet":
        """Return a new field set with merged fields (immutable operation)."""
        return FieldSet(self._fields + other._fields)

    @property
    def fields(self) -> List[Field]:
        """Get the list of fields."""
        return self._fields

    def empty(self) -> bool:
        """Check if the field set is empty."""
        return len(self._fields) == 0

    def __len__(self) -> int:
        """Get the number of fields."""
        return len(self._fields)

    def __iter__(self):
        """Iterate over fields."""
        return iter(self._fields)

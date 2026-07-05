"""Pydantic models defining the clinical extraction schema.

These models are the contract for the extraction pipeline: the LLM is
required to produce output in this shape, and anything malformed is
rejected at validation time rather than passed silently downstream.
"""

from enum import Enum

from pydantic import BaseModel, Field


class MedicationStatus(str, Enum):
    """Clinical status of an extracted medication."""

    ACTIVE = "active"
    DISCONTINUED = "discontinued"
    HISTORICAL = "historical"
    NEGATED = "negated"  # explicitly denied, e.g. "patient denies taking aspirin"
    UNKNOWN = "unknown"


class Medication(BaseModel):
    """A single medication mention extracted from a clinical note."""

    name: str = Field(
        description="Medication name exactly as written in the note"
    )
    dose: str | None = Field(
        default=None,
        description="Dose with units, e.g. '50 mg'. None if not stated in the note.",
    )
    route: str | None = Field(
        default=None,
        description="Route of administration, e.g. 'oral', 'IV'. None if not stated.",
    )
    frequency: str | None = Field(
        default=None,
        description="Frequency, e.g. 'twice daily', 'PRN'. None if not stated.",
    )
    status: MedicationStatus = Field(
        description=(
            "Whether the medication is active, discontinued, historical, "
            "negated, or unknown"
        )
    )
    evidence: str = Field(
        description=(
            "The exact sentence or phrase from the note supporting this "
            "extraction"
        )
    )


class ExtractionResult(BaseModel):
    """All medications extracted from a single clinical note."""

    medications: list[Medication] = Field(default_factory=list)

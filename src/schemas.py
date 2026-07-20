from typing import Optional
from pydantic import BaseModel, Field
from typing import Literal


class Demographics(BaseModel):
    sex: Optional[str] = Field(
        default=None,
        description="Patient's sex: 'male' or 'female'. null if not stated.",
    )

    age: Optional[float] = Field(
        default=None,
        description="Patient's age in years; may be fractional for infants "
        "(e.g. 0.03 for ~11 days old). null if not stated.",
    )

    weight_kg: Optional[float] = Field(
        default=None, description="Weight in kilograms. null if not stated."
    )
    height_cm: Optional[float] = Field(
        default=None, description="Height in centimeters. null if not stated."
    )
    bmi: Optional[float] = Field(
        default=None, description="Body mass index. null if not stated."
    )


class Symptom(BaseModel):
    name: str = Field(
        description="The symptom, e.g. 'chest pain', 'shortness of breath'."
    )
    negated: bool = Field(
        description="True if the note says the patient does NOT have it, "
        "e.g. 'denies chest pain'."
    )
    explicit: bool = Field(
        description="False if inferred from a description, "
        "e.g. 'winded walking' -> shortness of breath."
    )
    onset_or_duration: Optional[str] = Field(
        default=None, description="e.g. '3 days', 'sudden onset'. null if not stated."
    )
    severity: Optional[str] = Field(
        default=None, description="mild | moderate | severe, if stated. null otherwise."
    )


class LabTest(BaseModel):
    test_name: str = Field(description="___")
    sample_type: Optional[str] = Field(default=None, description="___")
    result_type: Optional[Literal["quantitative", "qualitative"]] = Field(
        default=None, description="___"
    )
    result: Optional[str] = Field(default=None, description="___")

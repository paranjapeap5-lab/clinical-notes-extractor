from typing import Optional
from pydantic import BaseModel, Field


class Demographics(BaseModel):
    sex: Optional[str] = Field(
        default=None,
        description="Patient's sex: 'male' or 'female'. null if not stated.",
    )
    age: Optional[int] = Field(
        default=None, description="Patient's age in years. null if not stated."
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

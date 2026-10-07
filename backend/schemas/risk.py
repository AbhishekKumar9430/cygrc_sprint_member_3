from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class RiskCreate(BaseModel):
    tenant_id: int = Field(..., ge=1)
    description: str = Field(..., min_length=5)
    owner: str = Field(..., min_length=2)
    likelihood: int = Field(..., ge=1, le=5)
    impact: int = Field(..., ge=1, le=5)
    treatment: str = Field(default="mitigate")


class RiskResponse(RiskCreate):
    model_config = ConfigDict(from_attributes=True)

    risk_id: int
    inherent_risk_score: int
    status: str = "open"
    is_closed: bool = False
    ciso_signoff: bool = False
    created_at: datetime | None = None
    closed_at: datetime | None = None


class RiskCloseRequest(BaseModel):
    ciso_signoff: bool = False


class DPDPBreachClockCreate(BaseModel):
    breach_detected_at: datetime
    notification_deadline_hours: int = Field(default=72, ge=1, le=168)
    jurisdiction: str = Field(default="IN")


class DPDPClockResponse(BaseModel):
    breach_detected_at: datetime
    deadline: datetime
    hours_remaining: int
    status: str
    jurisdiction: str
    message: str

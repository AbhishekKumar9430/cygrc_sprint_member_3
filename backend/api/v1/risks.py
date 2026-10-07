from datetime import datetime, timezone
from typing import Dict

from fastapi import APIRouter, HTTPException

from backend.models.risk import Risk
from backend.schemas.risk import RiskCloseRequest, RiskCreate, RiskResponse

router = APIRouter(prefix="/api/v1", tags=["risks"])

_in_memory_risks: Dict[int, Risk] = {}
_next_risk_id = 1


def _serialize_risk(risk: Risk) -> RiskResponse:
    return RiskResponse(
        risk_id=risk.risk_id,
        tenant_id=risk.tenant_id,
        description=risk.description,
        owner=risk.owner,
        likelihood=risk.likelihood,
        impact=risk.impact,
        inherent_risk_score=risk.inherent_risk_score,
        treatment=risk.treatment,
        status=risk.status,
        is_closed=risk.is_closed,
        ciso_signoff=risk.ciso_signoff,
        created_at=risk.created_at,
        closed_at=risk.closed_at,
    )


@router.get("/risks", response_model=list[RiskResponse])
def list_risks() -> list[RiskResponse]:
    return [_serialize_risk(risk) for risk in _in_memory_risks.values()]


@router.post("/risks", response_model=RiskResponse)
def create_risk(payload: RiskCreate) -> RiskResponse:
    global _next_risk_id

    risk = Risk(
        risk_id=_next_risk_id,
        tenant_id=payload.tenant_id,
        description=payload.description,
        owner=payload.owner,
        likelihood=payload.likelihood,
        impact=payload.impact,
        inherent_risk_score=payload.likelihood * payload.impact,
        treatment=payload.treatment,
        status="open",
        is_closed=False,
        ciso_signoff=False,
        created_at=datetime.now(timezone.utc),
        closed_at=None,
    )
    _in_memory_risks[risk.risk_id] = risk
    _next_risk_id += 1
    return _serialize_risk(risk)


@router.post("/risks/{risk_id}/close", response_model=RiskResponse)
def close_risk(risk_id: int, payload: RiskCloseRequest) -> RiskResponse:
    risk = _in_memory_risks.get(risk_id)
    if not risk:
        raise HTTPException(status_code=404, detail="Risk not found")

    if risk.inherent_risk_score >= 16 and not payload.ciso_signoff:
        raise HTTPException(
            status_code=403,
            detail="CISO sign-off required before closing high-risk items.",
        )

    risk.is_closed = True
    risk.status = "closed"
    risk.ciso_signoff = payload.ciso_signoff
    risk.closed_at = datetime.now(timezone.utc)
    return _serialize_risk(risk)

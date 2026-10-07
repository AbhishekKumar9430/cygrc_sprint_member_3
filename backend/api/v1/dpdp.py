from datetime import datetime, timedelta, timezone

from fastapi import APIRouter

from backend.models.risk import DPDPBreachClock
from backend.schemas.risk import DPDPBreachClockCreate, DPDPClockResponse

router = APIRouter(prefix="/api/v1", tags=["dpdp"])

_breach_clock: DPDPBreachClock | None = None


def _build_response(clock: DPDPBreachClock) -> DPDPClockResponse:
    now = datetime.now(timezone.utc)
    hours_remaining = int((clock.deadline - now).total_seconds() // 3600)
    if hours_remaining < 0:
        status = "breach_deadline_exceeded"
        message = "The 72-hour breach notification window has expired."
    elif hours_remaining <= 24:
        status = "critical"
        message = "Urgent action required: breach reporting deadline is within 24 hours."
    else:
        status = "active"
        message = "Breach clock is active and within the DPDP reporting window."

    return DPDPClockResponse(
        breach_detected_at=clock.breach_detected_at,
        deadline=clock.deadline,
        hours_remaining=max(hours_remaining, 0),
        status=status,
        jurisdiction=clock.jurisdiction,
        message=message,
    )


@router.get("/dpdp/breach-clock", response_model=DPDPClockResponse)
def get_breach_clock() -> DPDPClockResponse:
    global _breach_clock

    if _breach_clock is None:
        now = datetime.now(timezone.utc)
        clock = DPDPBreachClock(
            clock_id=1,
            tenant_id=1,
            breach_detected_at=now,
            deadline=now + timedelta(hours=72),
            hours_remaining=72,
            jurisdiction="IN",
            status="active",
            created_at=now,
        )
        _breach_clock = clock

    return _build_response(_breach_clock)


@router.post("/dpdp/breach-clock", response_model=DPDPClockResponse)
def create_breach_clock(payload: DPDPBreachClockCreate) -> DPDPClockResponse:
    global _breach_clock

    deadline = payload.breach_detected_at + timedelta(hours=payload.notification_deadline_hours)
    _breach_clock = DPDPBreachClock(
        clock_id=1,
        tenant_id=1,
        breach_detected_at=payload.breach_detected_at,
        deadline=deadline,
        hours_remaining=payload.notification_deadline_hours,
        jurisdiction=payload.jurisdiction,
        status="active",
        created_at=datetime.now(timezone.utc),
    )
    return _build_response(_breach_clock)

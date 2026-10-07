from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Risk(Base):
    __tablename__ = "risks"

    risk_id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, nullable=False, index=True)
    description = Column(String, nullable=False)
    owner = Column(String, nullable=False)
    likelihood = Column(Integer, nullable=False)
    impact = Column(Integer, nullable=False)
    inherent_risk_score = Column(Integer, nullable=False)
    treatment = Column(String, nullable=False, default="mitigate")
    status = Column(String, nullable=False, default="open")
    is_closed = Column(Boolean, nullable=False, default=False)
    ciso_signoff = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    closed_at = Column(DateTime(timezone=True), nullable=True)


class DPDPBreachClock(Base):
    __tablename__ = "dpdp_breach_clocks"

    clock_id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, nullable=False, default=1)
    breach_detected_at = Column(DateTime(timezone=True), nullable=False)
    deadline = Column(DateTime(timezone=True), nullable=False)
    hours_remaining = Column(Integer, nullable=False)
    jurisdiction = Column(String, nullable=False, default="IN")
    status = Column(String, nullable=False, default="open")
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


def test_risk_create_and_close_require_ciso_signoff_for_high_risk():
    create_response = client.post(
        "/api/v1/risks",
        json={
            "tenant_id": 1,
            "description": "Critical vendor access issue",
            "owner": "CISO",
            "likelihood": 4,
            "impact": 5,
            "treatment": "mitigate"
        },
    )
    assert create_response.status_code == 200, create_response.text
    body = create_response.json()
    assert body["inherent_risk_score"] == 20
    risk_id = body["risk_id"]

    close_response = client.post(
        f"/api/v1/risks/{risk_id}/close",
        json={"ciso_signoff": False},
    )
    assert close_response.status_code == 403, close_response.text
    assert "CISO sign-off" in close_response.json()["detail"]

    valid_close = client.post(
        f"/api/v1/risks/{risk_id}/close",
        json={"ciso_signoff": True},
    )
    assert valid_close.status_code == 200, valid_close.text
    assert valid_close.json()["status"] == "closed"


def test_dpdp_breach_clock_endpoints():
    get_response = client.get("/api/v1/dpdp/breach-clock")
    assert get_response.status_code == 200, get_response.text
    payload = get_response.json()
    assert "hours_remaining" in payload
    assert "deadline" in payload

    post_response = client.post(
        "/api/v1/dpdp/breach-clock",
        json={
            "breach_detected_at": "2026-10-07T09:00:00Z",
            "notification_deadline_hours": 72,
            "jurisdiction": "IN"
        },
    )
    assert post_response.status_code == 200, post_response.text
    clock = post_response.json()
    assert clock["hours_remaining"] >= 0
    assert clock["jurisdiction"] == "IN"

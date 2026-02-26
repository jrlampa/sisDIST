"""Tests for infrastructure domain — poles and conductors via HTTP client."""
import pytest
import pytest_asyncio


@pytest.mark.asyncio
async def test_list_poles_empty(client):
    resp = await client.get("/api/v1/infrastructure/poles")
    assert resp.status_code == 200
    assert resp.json() == []


@pytest.mark.asyncio
async def test_create_pole(client):
    payload = {
        "code": "P-001",
        "pole_type": "concreto",
        "latitude": -22.15018,
        "longitude": -42.92185,
        "elevation": 850.0,
        "pole_height": 11.0,
        "pole_class": "300",
        "owner": "Enel-RJ",
    }
    resp = await client.post("/api/v1/infrastructure/poles", json=payload)
    assert resp.status_code == 201
    data = resp.json()
    assert data["code"] == "P-001"
    assert data["id"] is not None


@pytest.mark.asyncio
async def test_get_pole(client):
    # Create first
    payload = {"code": "P-002", "pole_type": "madeira"}
    resp = await client.post("/api/v1/infrastructure/poles", json=payload)
    pole_id = resp.json()["id"]
    # Then get
    resp2 = await client.get(f"/api/v1/infrastructure/poles/{pole_id}")
    assert resp2.status_code == 200
    assert resp2.json()["code"] == "P-002"


@pytest.mark.asyncio
async def test_get_pole_not_found(client):
    resp = await client.get("/api/v1/infrastructure/poles/99999")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_update_pole(client):
    payload = {"code": "P-003", "pole_type": "concreto"}
    resp = await client.post("/api/v1/infrastructure/poles", json=payload)
    pole_id = resp.json()["id"]
    update = {"pole_height": 14.0, "observations": "Substituído em 2024"}
    resp2 = await client.put(f"/api/v1/infrastructure/poles/{pole_id}", json=update)
    assert resp2.status_code == 200
    assert resp2.json()["pole_height"] == 14.0


@pytest.mark.asyncio
async def test_delete_pole(client):
    payload = {"code": "P-DEL", "pole_type": "aço"}
    resp = await client.post("/api/v1/infrastructure/poles", json=payload)
    pole_id = resp.json()["id"]
    resp2 = await client.delete(f"/api/v1/infrastructure/poles/{pole_id}")
    assert resp2.status_code == 204
    resp3 = await client.get(f"/api/v1/infrastructure/poles/{pole_id}")
    assert resp3.status_code == 404


@pytest.mark.asyncio
async def test_list_conductors_empty(client):
    resp = await client.get("/api/v1/infrastructure/conductors")
    assert resp.status_code == 200
    assert resp.json() == []


@pytest.mark.asyncio
async def test_create_conductor(client):
    payload = {
        "conductor_type": "CA",
        "cross_section": 50.0,
        "voltage_level": "BT",
        "phases": 3,
        "length": 60.0,
    }
    resp = await client.post("/api/v1/infrastructure/conductors", json=payload)
    assert resp.status_code == 201
    data = resp.json()
    assert data["cross_section"] == 50.0
    assert data["conductor_type"] == "CA"


@pytest.mark.asyncio
async def test_get_conductor_not_found(client):
    resp = await client.get("/api/v1/infrastructure/conductors/99999")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_delete_conductor(client):
    payload = {"conductor_type": "CAA", "cross_section": 70.0, "voltage_level": "MT", "phases": 3}
    resp = await client.post("/api/v1/infrastructure/conductors", json=payload)
    conductor_id = resp.json()["id"]
    resp2 = await client.delete(f"/api/v1/infrastructure/conductors/{conductor_id}")
    assert resp2.status_code == 204

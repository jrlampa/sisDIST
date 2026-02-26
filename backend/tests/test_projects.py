"""Tests for projects domain."""
import pytest


@pytest.mark.asyncio
async def test_list_projects_empty(client):
    resp = await client.get("/api/v1/projects/")
    assert resp.status_code == 200
    assert resp.json() == []


@pytest.mark.asyncio
async def test_create_project(client):
    payload = {
        "name": "Rede MT Vila Nova",
        "description": "Extensão de rede MT no bairro Vila Nova",
        "concessionaire": "Enel-RJ",
    }
    resp = await client.post("/api/v1/projects/", json=payload)
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "Rede MT Vila Nova"
    assert data["concessionaire"] == "Enel-RJ"
    assert "id" in data


@pytest.mark.asyncio
async def test_get_project(client):
    payload = {"name": "Projeto Light Centro", "concessionaire": "Light"}
    resp = await client.post("/api/v1/projects/", json=payload)
    project_id = resp.json()["id"]
    resp2 = await client.get(f"/api/v1/projects/{project_id}")
    assert resp2.status_code == 200
    assert resp2.json()["concessionaire"] == "Light"


@pytest.mark.asyncio
async def test_get_project_not_found(client):
    resp = await client.get("/api/v1/projects/99999")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_update_project(client):
    payload = {"name": "Projeto Antigo", "concessionaire": "Enel-RJ"}
    resp = await client.post("/api/v1/projects/", json=payload)
    project_id = resp.json()["id"]
    update = {"name": "Projeto Atualizado", "description": "Nova descrição"}
    resp2 = await client.put(f"/api/v1/projects/{project_id}", json=update)
    assert resp2.status_code == 200
    assert resp2.json()["name"] == "Projeto Atualizado"


@pytest.mark.asyncio
async def test_delete_project(client):
    payload = {"name": "Projeto para deletar", "concessionaire": "Light"}
    resp = await client.post("/api/v1/projects/", json=payload)
    project_id = resp.json()["id"]
    resp2 = await client.delete(f"/api/v1/projects/{project_id}")
    assert resp2.status_code == 204
    resp3 = await client.get(f"/api/v1/projects/{project_id}")
    assert resp3.status_code == 404


@pytest.mark.asyncio
async def test_material_list(client):
    payload = {"name": "Projeto Material Test", "concessionaire": "Enel-RJ"}
    resp = await client.post("/api/v1/projects/", json=payload)
    project_id = resp.json()["id"]
    resp2 = await client.get(f"/api/v1/projects/{project_id}/material-list")
    assert resp2.status_code == 200
    data = resp2.json()
    assert data["projeto_id"] == project_id
    assert "items" in data


@pytest.mark.asyncio
async def test_material_list_not_found(client):
    resp = await client.get("/api/v1/projects/99999/material-list")
    assert resp.status_code == 404

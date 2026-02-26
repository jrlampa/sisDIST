"""Additional tests for service layers and mapping service to improve coverage."""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from app.domains.mapping.service import MappingService
from app.domains.mapping.schemas import OSMResponse, OSMNode


class TestMappingServiceFetchOSM:
    """Test MappingService.fetch_osm_data (mocked)."""

    @pytest.mark.asyncio(mode="auto")
    async def test_fetch_osm_delegates_to_osm_service(self):
        svc = MappingService()
        fake = OSMResponse(poles=[], towers=[], power_lines=[], substations=[], total_elements=0)
        with patch("app.domains.mapping.service.fetch_osm_data", new=AsyncMock(return_value=fake)):
            result = await svc.fetch_osm_data(-22.15018, -42.92185, 500)
        assert result.total_elements == 0

    @pytest.mark.asyncio(mode="auto")
    async def test_fetch_osm_returns_poles(self):
        svc = MappingService()
        node = OSMNode(osm_id=1, lat=-22.15, lon=-42.92, tags={"power": "pole"})
        fake = OSMResponse(poles=[node], towers=[], power_lines=[], substations=[], total_elements=1)
        with patch("app.domains.mapping.service.fetch_osm_data", new=AsyncMock(return_value=fake)):
            result = await svc.fetch_osm_data(-22.15, -42.92, 100)
        assert len(result.poles) == 1
        assert result.poles[0].osm_id == 1


class TestMappingServiceElevation:
    """Test MappingService.fetch_elevation (mocked httpx)."""

    @pytest.mark.asyncio(mode="auto")
    async def test_fetch_elevation_returns_response(self):
        svc = MappingService()
        fake_json = {"results": [{"elevation": 850.5, "location": {"lat": -22.15018, "lng": -42.92185}}]}
        mock_resp = MagicMock()
        mock_resp.raise_for_status = MagicMock()
        mock_resp.json.return_value = fake_json

        mock_client = AsyncMock()
        mock_client.get = AsyncMock(return_value=mock_resp)

        with patch("app.domains.mapping.service.httpx.AsyncClient") as mock_cls:
            mock_cls.return_value.__aenter__ = AsyncMock(return_value=mock_client)
            mock_cls.return_value.__aexit__ = AsyncMock(return_value=False)
            result = await svc.fetch_elevation(-22.15018, -42.92185)

        assert result.elevation == pytest.approx(850.5)
        assert result.lat == pytest.approx(-22.15018)
        assert result.lon == pytest.approx(-42.92185)

    @pytest.mark.asyncio(mode="auto")
    async def test_fetch_elevation_zero(self):
        svc = MappingService()
        fake_json = {"results": [{"elevation": 0.0, "location": {"lat": 0.0, "lng": 0.0}}]}
        mock_resp = MagicMock()
        mock_resp.raise_for_status = MagicMock()
        mock_resp.json.return_value = fake_json

        mock_client = AsyncMock()
        mock_client.get = AsyncMock(return_value=mock_resp)

        with patch("app.domains.mapping.service.httpx.AsyncClient") as mock_cls:
            mock_cls.return_value.__aenter__ = AsyncMock(return_value=mock_client)
            mock_cls.return_value.__aexit__ = AsyncMock(return_value=False)
            result = await svc.fetch_elevation(0.0, 0.0)

        assert result.elevation == 0.0


class TestMappingServiceUTMNorthern:
    """Test UTM conversion for northern hemisphere."""

    def test_convert_northern_hemisphere_uses_north_epsg(self):
        svc = MappingService()
        # A point in Zone 18N (roughly eastern USA/Canada)
        result = svc.convert_utm_to_wgs84(500000.0, 4500000.0, 18, "N")
        # Northern hemisphere → positive latitude
        assert result.lat > 0
        assert result.hemisphere == "N"
        assert result.zone == 18

    def test_convert_utm_epsg_south_zone23(self):
        svc = MappingService()
        result = svc.convert_utm_to_wgs84(714316.0, 7549084.0, 23, "S")
        # SIRGAS2000 zone 23S = EPSG 31983
        assert result.epsg == 31983

    def test_convert_utm_epsg_north_zone18(self):
        svc = MappingService()
        result = svc.convert_utm_to_wgs84(500000.0, 4500000.0, 18, "N")
        # Northern formula: 31954 + 18 = 31972
        assert result.epsg == 31972


class TestMappingServiceValidation:
    """Test input validation for lat/lon and radius."""

    @pytest.mark.asyncio(mode="auto")
    async def test_fetch_osm_invalid_lat(self):
        from fastapi import HTTPException
        svc = MappingService()
        with pytest.raises(HTTPException) as exc_info:
            await svc.fetch_osm_data(95.0, -42.92185, 500)
        assert exc_info.value.status_code == 422

    @pytest.mark.asyncio(mode="auto")
    async def test_fetch_osm_invalid_lon(self):
        from fastapi import HTTPException
        svc = MappingService()
        with pytest.raises(HTTPException) as exc_info:
            await svc.fetch_osm_data(-22.15, 200.0, 500)
        assert exc_info.value.status_code == 422

    @pytest.mark.asyncio(mode="auto")
    async def test_fetch_osm_radius_too_small(self):
        from fastapi import HTTPException
        svc = MappingService()
        with pytest.raises(HTTPException) as exc_info:
            await svc.fetch_osm_data(-22.15, -42.92, 10)
        assert exc_info.value.status_code == 422

    @pytest.mark.asyncio(mode="auto")
    async def test_fetch_osm_radius_too_large(self):
        from fastapi import HTTPException
        svc = MappingService()
        with pytest.raises(HTTPException) as exc_info:
            await svc.fetch_osm_data(-22.15, -42.92, 99999)
        assert exc_info.value.status_code == 422

    @pytest.mark.asyncio(mode="auto")
    async def test_fetch_elevation_invalid_lat(self):
        from fastapi import HTTPException
        svc = MappingService()
        with pytest.raises(HTTPException) as exc_info:
            await svc.fetch_elevation(-91.0, -42.92185)
        assert exc_info.value.status_code == 422


class TestInfrastructureServiceDirect:
    """Test InfrastructureService methods directly with a db session."""

    @pytest.mark.asyncio(mode="auto")
    async def test_list_poles_with_items(self, db_session):
        from app.domains.infrastructure.service import InfrastructureService
        from app.domains.infrastructure.schemas import PoleCreate

        svc = InfrastructureService(db_session)
        payload = PoleCreate(code="P-SVC-01", pole_type="concreto")
        await svc.create_pole(payload)

        poles = await svc.list_poles()
        assert len(poles) == 1
        assert poles[0].code == "P-SVC-01"

    @pytest.mark.asyncio(mode="auto")
    async def test_get_pole_returns_none_for_missing(self, db_session):
        from app.domains.infrastructure.service import InfrastructureService

        svc = InfrastructureService(db_session)
        result = await svc.get_pole(99999)
        assert result is None

    @pytest.mark.asyncio(mode="auto")
    async def test_get_pole_returns_created(self, db_session):
        from app.domains.infrastructure.service import InfrastructureService
        from app.domains.infrastructure.schemas import PoleCreate

        svc = InfrastructureService(db_session)
        created = await svc.create_pole(PoleCreate(code="P-SVC-02", pole_type="madeira"))
        fetched = await svc.get_pole(created.id)
        assert fetched is not None
        assert fetched.code == "P-SVC-02"

    @pytest.mark.asyncio(mode="auto")
    async def test_update_pole_returns_none_for_missing(self, db_session):
        from app.domains.infrastructure.service import InfrastructureService
        from app.domains.infrastructure.schemas import PoleUpdate

        svc = InfrastructureService(db_session)
        result = await svc.update_pole(99999, PoleUpdate(pole_height=12.0))
        assert result is None

    @pytest.mark.asyncio(mode="auto")
    async def test_update_pole_updates_fields(self, db_session):
        from app.domains.infrastructure.service import InfrastructureService
        from app.domains.infrastructure.schemas import PoleCreate, PoleUpdate

        svc = InfrastructureService(db_session)
        created = await svc.create_pole(PoleCreate(code="P-SVC-03", pole_type="aço"))
        updated = await svc.update_pole(created.id, PoleUpdate(pole_height=14.0, observations="Teste"))
        assert updated is not None
        assert updated.pole_height == 14.0

    @pytest.mark.asyncio(mode="auto")
    async def test_delete_pole_returns_false_for_missing(self, db_session):
        from app.domains.infrastructure.service import InfrastructureService

        svc = InfrastructureService(db_session)
        result = await svc.delete_pole(99999)
        assert result is False

    @pytest.mark.asyncio(mode="auto")
    async def test_delete_pole_returns_true_and_removes(self, db_session):
        from app.domains.infrastructure.service import InfrastructureService
        from app.domains.infrastructure.schemas import PoleCreate

        svc = InfrastructureService(db_session)
        created = await svc.create_pole(PoleCreate(code="P-SVC-DEL", pole_type="concreto"))
        deleted = await svc.delete_pole(created.id)
        assert deleted is True
        assert await svc.get_pole(created.id) is None

    @pytest.mark.asyncio(mode="auto")
    async def test_list_conductors_with_items(self, db_session):
        from app.domains.infrastructure.service import InfrastructureService
        from app.domains.infrastructure.schemas import ConductorCreate

        svc = InfrastructureService(db_session)
        await svc.create_conductor(
            ConductorCreate(conductor_type="CA", cross_section=50.0, voltage_level="BT", phases=3)
        )
        conductors = await svc.list_conductors()
        assert len(conductors) == 1
        assert conductors[0].conductor_type == "CA"

    @pytest.mark.asyncio(mode="auto")
    async def test_get_conductor_returns_none_for_missing(self, db_session):
        from app.domains.infrastructure.service import InfrastructureService

        svc = InfrastructureService(db_session)
        result = await svc.get_conductor(99999)
        assert result is None

    @pytest.mark.asyncio(mode="auto")
    async def test_update_conductor_returns_none_for_missing(self, db_session):
        from app.domains.infrastructure.service import InfrastructureService
        from app.domains.infrastructure.schemas import ConductorUpdate

        svc = InfrastructureService(db_session)
        result = await svc.update_conductor(99999, ConductorUpdate(length=100.0))
        assert result is None

    @pytest.mark.asyncio(mode="auto")
    async def test_update_conductor_updates_fields(self, db_session):
        from app.domains.infrastructure.service import InfrastructureService
        from app.domains.infrastructure.schemas import ConductorCreate, ConductorUpdate

        svc = InfrastructureService(db_session)
        created = await svc.create_conductor(
            ConductorCreate(conductor_type="CAA", cross_section=70.0, voltage_level="MT", phases=3)
        )
        updated = await svc.update_conductor(created.id, ConductorUpdate(length=150.0))
        assert updated is not None
        assert updated.length == 150.0

    @pytest.mark.asyncio(mode="auto")
    async def test_delete_conductor_returns_false_for_missing(self, db_session):
        from app.domains.infrastructure.service import InfrastructureService

        svc = InfrastructureService(db_session)
        result = await svc.delete_conductor(99999)
        assert result is False

    @pytest.mark.asyncio(mode="auto")
    async def test_delete_conductor_returns_true_and_removes(self, db_session):
        from app.domains.infrastructure.service import InfrastructureService
        from app.domains.infrastructure.schemas import ConductorCreate

        svc = InfrastructureService(db_session)
        created = await svc.create_conductor(
            ConductorCreate(conductor_type="CA", cross_section=35.0, voltage_level="BT", phases=1)
        )
        deleted = await svc.delete_conductor(created.id)
        assert deleted is True
        assert await svc.get_conductor(created.id) is None


class TestProjectsServiceDirect:
    """Test ProjectService methods directly with a db session."""

    @pytest.mark.asyncio(mode="auto")
    async def test_list_projects_with_items(self, db_session):
        from app.domains.projects.service import ProjectService
        from app.domains.projects.schemas import ProjectCreate

        svc = ProjectService(db_session)
        await svc.create_project(ProjectCreate(name="Projeto Teste", concessionaire="Enel-RJ"))
        projects = await svc.list_projects()
        assert len(projects) == 1
        assert projects[0].name == "Projeto Teste"

    @pytest.mark.asyncio(mode="auto")
    async def test_get_project_returns_none_for_missing(self, db_session):
        from app.domains.projects.service import ProjectService

        svc = ProjectService(db_session)
        result = await svc.get_project(99999)
        assert result is None

    @pytest.mark.asyncio(mode="auto")
    async def test_get_project_returns_created(self, db_session):
        from app.domains.projects.service import ProjectService
        from app.domains.projects.schemas import ProjectCreate

        svc = ProjectService(db_session)
        created = await svc.create_project(ProjectCreate(name="Proj-A", concessionaire="Light"))
        fetched = await svc.get_project(created.id)
        assert fetched is not None
        assert fetched.name == "Proj-A"

    @pytest.mark.asyncio(mode="auto")
    async def test_update_project_returns_none_for_missing(self, db_session):
        from app.domains.projects.service import ProjectService
        from app.domains.projects.schemas import ProjectUpdate

        svc = ProjectService(db_session)
        result = await svc.update_project(99999, ProjectUpdate(name="X"))
        assert result is None

    @pytest.mark.asyncio(mode="auto")
    async def test_update_project_updates_fields(self, db_session):
        from app.domains.projects.service import ProjectService
        from app.domains.projects.schemas import ProjectCreate, ProjectUpdate

        svc = ProjectService(db_session)
        created = await svc.create_project(ProjectCreate(name="Original", concessionaire="Enel-RJ"))
        updated = await svc.update_project(created.id, ProjectUpdate(name="Atualizado"))
        assert updated is not None
        assert updated.name == "Atualizado"

    @pytest.mark.asyncio(mode="auto")
    async def test_delete_project_returns_false_for_missing(self, db_session):
        from app.domains.projects.service import ProjectService

        svc = ProjectService(db_session)
        result = await svc.delete_project(99999)
        assert result is False

    @pytest.mark.asyncio(mode="auto")
    async def test_delete_project_returns_true_and_removes(self, db_session):
        from app.domains.projects.service import ProjectService
        from app.domains.projects.schemas import ProjectCreate

        svc = ProjectService(db_session)
        created = await svc.create_project(ProjectCreate(name="Para Deletar", concessionaire="Light"))
        deleted = await svc.delete_project(created.id)
        assert deleted is True
        assert await svc.get_project(created.id) is None

    @pytest.mark.asyncio(mode="auto")
    async def test_generate_material_list_returns_none_for_missing(self, db_session):
        from app.domains.projects.service import ProjectService

        svc = ProjectService(db_session)
        result = await svc.generate_material_list(99999)
        assert result is None

    @pytest.mark.asyncio(mode="auto")
    async def test_generate_material_list_returns_dict(self, db_session):
        from app.domains.projects.service import ProjectService
        from app.domains.projects.schemas import ProjectCreate

        svc = ProjectService(db_session)
        created = await svc.create_project(ProjectCreate(name="ML Test", concessionaire="Enel-RJ"))
        result = await svc.generate_material_list(created.id)
        assert result is not None
        assert result["projeto_id"] == created.id
        assert result["concessionaire"] == "Enel-RJ"
        assert "items" in result

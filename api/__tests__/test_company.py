import pytest
from model import Company
from httpx import AsyncClient


class TestReadAll:
    @pytest.mark.asyncio
    async def test_success(self, test_client: AsyncClient):
        # Arrange
        await Company.create_new("test_company")

        # Act
        response = await test_client.get('/api/v1/company')

        # Assert
        assert response.status_code == 200
        json = response.json()[0]

        assert isinstance(json.get('_id'), str)
        assert json.get('name') == 'test_company'

    @pytest.mark.asyncio
    async def test_success_empty(self, test_client: AsyncClient):
        # Act
        response = await test_client.get('/api/v1/company')

        # Assert
        assert response.status_code == 200
        assert response.json() == []


class TestCreate:
    @pytest.mark.asyncio
    async def test_success(self, test_client: AsyncClient):
        # Act
        response = await test_client.post('/api/v1/company', json={
            "name": "test_company"
        })

        # Assert
        assert response.status_code == 201
        json = response.json()

        assert isinstance(json.get('_id'), str)
        assert json.get('name') == 'test_company'

    @pytest.mark.asyncio
    async def test_fail_name_too_short(self, test_client: AsyncClient):
        # Act
        response = await test_client.post('/api/v1/company', json={
            "name": ""
        })

        # Assert
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_fail_name_too_long(self, test_client: AsyncClient):
        # Act
        response = await test_client.post('/api/v1/company', json={
            "name": "test_company_this_name_is_way_too_long_like_way_tooooooooooo_long"
        })

        # Assert
        assert response.status_code == 422


class TestGet:
    @pytest.mark.asyncio
    async def test_success(self, test_client: AsyncClient):
        # Arrange
        company = await Company.create_new("test_company")

        # Act
        response = await test_client.get(f'/api/v1/company/{company.id}')

        # Assert
        assert response.status_code == 200
        json = response.json()

        assert isinstance(json.get('_id'), str)
        assert json.get('name') == 'test_company'

    @pytest.mark.asyncio
    async def test_fail_not_found(self, test_client: AsyncClient):
        # Act
        response = await test_client.get(f'/api/v1/company/646299009ae04213efcf0a31')

        # Assert
        assert response.status_code == 404


class TestUpdate:
    @pytest.mark.asyncio
    async def test_success(self, test_client: AsyncClient):
        # Arrange
        company = await Company.create_new("test_company")

        # Act
        response = await test_client.put(f'/api/v1/company/{company.id}', json={
            "name": "updated_name_test_company"
        })

        # Assert
        assert response.status_code == 201
        json = response.json()

        assert isinstance(json.get('_id'), str)
        assert json.get('name') == 'updated_name_test_company'

    @pytest.mark.asyncio
    async def test_fail_not_found(self, test_client: AsyncClient):
        # Act
        response = await test_client.put(f'/api/v1/company/646299009ae04213efcf0a31', json={
            "name": "not found"
        })

        # Assert
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_fail_name_too_short(self, test_client: AsyncClient):
        # Arrange
        company = await Company.create_new("test_company")

        # Act
        response = await test_client.put(f'/api/v1/company/{company.id}', json={
            "name": ""
        })

        # Assert
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_fail_name_too_long(self, test_client: AsyncClient):
        # Arrange
        company = await Company.create_new("test_company")

        # Act
        response = await test_client.put(f'/api/v1/company/{company.id}', json={
            "name": "test_company_this_name_is_way_too_long_like_way_tooooooooooo_long"
        })

        # Assert
        assert response.status_code == 422


class TestDelete:
    @pytest.mark.asyncio
    async def test_success(self, test_client: AsyncClient):
        # Arrange
        company = await Company.create_new("test_company")

        # Act
        response = await test_client.delete(f'/api/v1/company/{company.id}')

        # Assert
        assert response.status_code == 201

    @pytest.mark.asyncio
    async def test_fail_not_found(self, test_client: AsyncClient):
        # Act
        response = await test_client.delete(f'/api/v1/company/646299009ae04213efcf0a31')

        # Assert
        assert response.status_code == 404


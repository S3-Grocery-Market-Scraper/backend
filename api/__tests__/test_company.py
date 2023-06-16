import pytest
from model import Company
from httpx import AsyncClient
from datetime import datetime


def is_datetime(input: str):
    try:
        return datetime.strptime(input, "%Y-%m-%dT%H:%M:%S.%f")
    except ValueError:
        return False


class TestCompanies:
    @pytest.mark.asyncio
    async def test_success(self, test_client: AsyncClient):
        # Arrange
        await Company.create_new("test_company", "Test company")

        # Act
        response = await test_client.post('/api/graphql', json={
            'query': """query {
                companies {
                    _id
                    code
                    name
                    createdOn
                    lastModified
                }
            }
            """
        })

        # Assert
        assert response.status_code == 200
        json = response.json().get('data').get('companies')[0]

        assert isinstance(json.get('_id'), str)
        assert json.get('code') == 'test_company'
        assert json.get('name') == 'Test company'
        assert is_datetime(json.get('createdOn'))
        assert is_datetime(json.get('lastModified'))

    @pytest.mark.asyncio
    async def test_success_filter_code(self, test_client: AsyncClient):
        # Arrange
        await Company.create_new("lidl", "Lidl")
        await Company.create_new("spar", "Spar supermarkt")
        await Company.create_new("albert_heijn", "Albert Heijn")
        await Company.create_new("albert_heijn_to_go", "AH to go")
        await Company.create_new("jumbo", "Jumbo supermarkten")

        # Act
        response = await test_client.post('/api/graphql', json={
            'query': """query {
                companies(code: "albert_heijn") {
                    _id
                    code
                    name
                    createdOn
                    lastModified
                }
            }
            """
        })

        # Assert
        assert response.status_code == 200
        assert len(response.json().get('data').get('companies')) == 2

    @pytest.mark.asyncio
    async def test_success_filter_name(self, test_client: AsyncClient):
        # Arrange
        await Company.create_new("lidl", "Lidl")
        await Company.create_new("spar", "Spar supermarkt")
        await Company.create_new("albert_heijn", "Albert Heijn")
        await Company.create_new("albert_heijn_to_go", "AH to go")
        await Company.create_new("jumbo", "Jumbo supermarkten")

        # Act
        response = await test_client.post('/api/graphql', json={
            'query': """query {
                companies(name: "supermarkt") {
                    _id
                    code
                    name
                    createdOn
                    lastModified
                }
            }
            """
        })

        # Assert
        assert response.status_code == 200
        assert len(response.json().get('data').get('companies')) == 2

    @pytest.mark.asyncio
    async def test_success_limit(self, test_client: AsyncClient):
        # Arrange
        await Company.create_new("test_company", "Test company")
        await Company.create_new("test_company2", "Test company")
        await Company.create_new("test_company3", "Test company")
        await Company.create_new("test_company4", "Test company")
        await Company.create_new("test_company5", "Test company")
        await Company.create_new("test_company6", "Test company")

        # Act
        response = await test_client.post('/api/graphql', json={
            'query': """query {
                companies(limit: 5) {
                    _id
                    code
                    name
                    createdOn
                    lastModified
                }
            }
            """
        })

        # Assert
        assert response.status_code == 200
        assert len(response.json().get('data').get('companies')) == 5

    @pytest.mark.asyncio
    async def test_success_offset(self, test_client: AsyncClient):
        # Arrange
        await Company.create_new("test_company", "Test company")
        await Company.create_new("test_company2", "Test company")
        await Company.create_new("test_company3", "Test company")
        await Company.create_new("test_company4", "Test company")
        await Company.create_new("test_company5", "Test company")
        await Company.create_new("test_company6", "Test company")

        # Act
        response = await test_client.post('/api/graphql', json={
            'query': """query {
                companies(offset: 5) {
                    _id
                    code
                    name
                    createdOn
                    lastModified
                }
            }
            """
        })

        # Assert
        assert response.status_code == 200
        assert len(response.json().get('data').get('companies')) == 1

    @pytest.mark.asyncio
    async def test_success_sort_code(self, test_client: AsyncClient):
        # Arrange
        await Company.create_new("test_company", "AAA")
        await Company.create_new("test_company2", "BBB")
        await Company.create_new("test_company3", "CCC")

        # Act
        response = await test_client.post('/api/graphql', json={
            'query': """query {
                companies(sort: [["code", "desc"]]) {
                    _id
                    code
                    name
                    createdOn
                    lastModified
                }
            }
            """
        })

        # Assert
        assert response.status_code == 200
        json = response.json().get('data').get('companies')[0]

        assert isinstance(json.get('_id'), str)
        assert json.get('code') == 'test_company3'
        assert json.get('name') == 'CCC'
        assert is_datetime(json.get('createdOn'))
        assert is_datetime(json.get('lastModified'))

    @pytest.mark.asyncio
    async def test_success_sort_name(self, test_client: AsyncClient):
        # Arrange
        await Company.create_new("test_company", "AAA")
        await Company.create_new("test_company2", "BBB")
        await Company.create_new("test_company3", "CCC")

        # Act
        response = await test_client.post('/api/graphql', json={
            'query': """query {
                companies(sort: [["name", "desc"]]) {
                    _id
                    code
                    name
                    createdOn
                    lastModified
                }
            }
            """
        })

        # Assert
        assert response.status_code == 200
        json = response.json().get('data').get('companies')[0]

        assert isinstance(json.get('_id'), str)
        assert json.get('code') == 'test_company3'
        assert json.get('name') == 'CCC'
        assert is_datetime(json.get('createdOn'))
        assert is_datetime(json.get('lastModified'))

    @pytest.mark.asyncio
    async def test_success_empty(self, test_client: AsyncClient):
        # Act
        response = await test_client.post('/api/graphql', json={
            'query': """query {
                companies {
                    _id
                    code
                    name
                    createdOn
                    lastModified
                }
            }
            """
        })

        # Assert
        assert response.status_code == 200
        assert response.json() == {'data': {'companies': []}}


class TestCompanyGetById:
    @pytest.mark.asyncio
    async def test_success(self, test_client: AsyncClient):
        # Arrange
        company = await Company.create_new("test_company", "Test company")

        # Act
        response = await test_client.post('/api/graphql', json={
            'query': f"""query {{
                companyById(id: "{company.id}") {{
                    _id
                    code
                    name
                    createdOn
                    lastModified
                }}
            }}
            """
        })

        # Assert
        assert response.status_code == 200
        json = response.json().get('data').get('companyById')

        assert isinstance(json.get('_id'), str)
        assert json.get('code') == 'test_company'
        assert json.get('name') == 'Test company'
        assert is_datetime(json.get('createdOn'))
        assert is_datetime(json.get('lastModified'))

    @pytest.mark.asyncio
    async def test_fail_not_found(self, test_client: AsyncClient):
        # Act
        response = await test_client.post('/api/graphql', json={
            'query': f"""query {{
                companyById(id: "6488d550a2117f0d2e1aaddd") {{
                    _id
                    code
                    name
                    createdOn
                    lastModified
                }}
            }}
            """
        })

        # Assert
        assert response.status_code == 200
        assert response.json() == {'data': {'companyById': None}}


class TestCompanyGetByCode:
    @pytest.mark.asyncio
    async def test_success(self, test_client: AsyncClient):
        # Arrange
        company = await Company.create_new("test_company", "Test company")

        # Act
        response = await test_client.post('/api/graphql', json={
            'query': f"""query {{
                companyByCode(code: "{company.code}") {{
                    _id
                    code
                    name
                    createdOn
                    lastModified
                }}
            }}
            """
        })

        # Assert
        assert response.status_code == 200
        json = response.json().get('data').get('companyByCode')

        assert isinstance(json.get('_id'), str)
        assert json.get('code') == 'test_company'
        assert json.get('name') == 'Test company'
        assert is_datetime(json.get('createdOn'))
        assert is_datetime(json.get('lastModified'))

    @pytest.mark.asyncio
    async def test_fail_not_found(self, test_client: AsyncClient):
        # Act
        response = await test_client.post('/api/graphql', json={
            'query': f"""query {{
                companyByCode(code: "some_code_that_doesnt_exist") {{
                    _id
                    code
                    name
                    createdOn
                    lastModified
                }}
            }}
            """
        })

        # Assert
        assert response.status_code == 200
        assert response.json() == {'data': {'companyByCode': None}}

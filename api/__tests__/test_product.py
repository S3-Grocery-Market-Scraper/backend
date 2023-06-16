# import pytest
# from model import Company, Product
#
#
# class TestReadAll:
#     @pytest.mark.asyncio
#     async def test_success(self, test_client):
#         # Arrange
#         company = await Company.create_new("test_company")
#         await Product.create_new(company=company, name="Banana", price=6.99)
#
#         # response = await test_client.post('/api/v1/company', json={
#         #     "name": "test_company"
#         # })
#         # response2 = await test_client.post(f'/api/v1/company/{response.json()["_id"]}/product', json={
#         #     "name": "Banana",
#         #     "price": 6.99
#         # })
#         # print("RESPONSE DATA", response2.json())
#         # print(test_client.get(f'/api/v1/company/{response.json()["_id"]}/product').json())
#
#         # Act
#         response = await test_client.get(f'/api/v1/company/{company.id}/product')
#         #response = await test_client.get(f'/api/v1/company/{response.json()["_id"]}/product')
#
#         # Assert
#         assert response.status_code == 200
#         json = response.json()
#         print(json)
#
#         assert json == [{}]

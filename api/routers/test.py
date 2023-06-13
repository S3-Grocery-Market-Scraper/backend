from fastapi import APIRouter, HTTPException
from model import Company, ProductModel, Category, ProductItem

router = APIRouter()


@router.post("/test", status_code=201)
async def product_create():
    jumbo = await Company.create_new("Jumbo")
    ah = await Company.create_new("Albert Heijn")

    beer = await Category.create_new("Bier")
    vegetable = await Category.create_new("Groente")
    pizza = await Category.create_new("Pizza")
    fried = await Category.create_new("Frituur")
    freezer = await Category.create_new("Diepvries")

    heineken = await ProductModel.create_new("Heineken", [beer])
    amstel = await ProductModel.create_new("Amstel", [beer])
    radler = await ProductModel.create_new("Radler", [beer])
    grolsch = await ProductModel.create_new("Grolsch", [beer])

    tomaat = await ProductModel.create_new("Tomaat", [vegetable])
    avocado = await ProductModel.create_new("Avocado", [vegetable])
    komkommer = await ProductModel.create_new("Komkommer", [vegetable])

    pizza_salami = await ProductModel.create_new("Pizza Salami", [pizza, freezer])
    pizza_hawaii = await ProductModel.create_new("Pizza Hawaii", [pizza, freezer])
    pizza_kip = await ProductModel.create_new("Verse pizza kippenvlees", [pizza])

    frikandel = await ProductModel.create_new("Frikandel", [fried, freezer])

    await ProductItem.create_new(company=ah, product_model=heineken, price=17.56)
    await ProductItem.create_new(company=jumbo, product_model=heineken, price=16.89)

    await ProductItem.create_new(company=ah, product_model=amstel, price=6.88)
    await ProductItem.create_new(company=jumbo, product_model=amstel, price=18.99)

    await ProductItem.create_new(company=ah, product_model=radler, price=16.46)
    await ProductItem.create_new(company=jumbo, product_model=radler, price=17.79)

    await ProductItem.create_new(company=ah, product_model=grolsch, price=19.46)
    await ProductItem.create_new(company=jumbo, product_model=grolsch, price=15.99)

    await ProductItem.create_new(company=ah, product_model=tomaat, price=0.99)
    await ProductItem.create_new(company=jumbo, product_model=tomaat, price=0.89)

    await ProductItem.create_new(company=ah, product_model=avocado, price=0.99)
    await ProductItem.create_new(company=jumbo, product_model=avocado, price=1.09)

    await ProductItem.create_new(company=ah, product_model=komkommer, price=1.09)
    await ProductItem.create_new(company=jumbo, product_model=komkommer, price=1.05)

    await ProductItem.create_new(company=ah, product_model=pizza_salami, price=2.99)
    await ProductItem.create_new(company=jumbo, product_model=pizza_salami, price=3.09)

    await ProductItem.create_new(company=ah, product_model=pizza_hawaii, price=1.89)
    await ProductItem.create_new(company=jumbo, product_model=pizza_hawaii, price=2.19)

    await ProductItem.create_new(company=ah, product_model=pizza_kip, price=3.95)
    await ProductItem.create_new(company=jumbo, product_model=pizza_kip, price=3.99)

    await ProductItem.create_new(company=ah, product_model=frikandel, price=2.99)
    await ProductItem.create_new(company=jumbo, product_model=frikandel, price=2.99)

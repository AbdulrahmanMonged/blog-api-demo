from typing import Optional
from fastapi import APIRouter, Cookie, Header, Response, status
from fastapi.responses import HTMLResponse, PlainTextResponse

router = APIRouter(prefix="/product", tags=["product"])

products = ["phone", "tv", "pc"]


@router.get("/all")
async def get_all_products():
    converted_text = " ".join(products)
    return Response(content=converted_text, media_type="text/plain")

@router.get("/withheader")
async def get_product_with_headers(response: Response, custom_headers: Optional[list[str]] = Header(None)):
    response.headers['custom-header'] = ", ".join(custom_headers)
    return products



@router.get("/set_cookie")
async def cookie_example(response: Response, simple_cookie_key: Optional[str] = Cookie(None)):
    response.set_cookie(key="simple_cookie_key", value="simple_cookie_value")
    return {"detail": "Cookie has been set successfully", "result": simple_cookie_key}

@router.get(
    "/{id}",
    responses={
        200: {
            "content": {"text/html": {"example": "<div>Product</div>"}},
            "description": "Returns a html response of a product",
        },
        404: {
            "content": {"text/plain": {"example": "Product Not found"}},
            "description": "Returns a cleartext of a product not found",
        },
    }
)
async def get_product(id: int):
    if id >= len(products):
        out = "Prodyct not found"
        return PlainTextResponse(
            content=out, media_type="text/plain", status_code=status.HTTP_404_NOT_FOUND
        )
    out = f"""
    <head>
        <style>
        .product {{
            width: 500px;
            height: 30px;
            border: 2px inset green;
            background-color: lightblue;
            text-align: center
        }}
        </style>
    </head>
    <div class="product"><em>Random Product</em></div>
    """
    return HTMLResponse(content=out, media_type="text/html")

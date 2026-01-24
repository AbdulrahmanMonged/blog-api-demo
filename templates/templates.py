from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from schemas import ProductBase

router = APIRouter(prefix="/templates", tags=['templates'])
templates = Jinja2Templates(directory="templates")


@router.post("/product/{id}", response_class=HTMLResponse)
async def get_product(id: int,  product: ProductBase, request: Request):
    return templates.TemplateResponse("product.html", {
        "request": request,
        "id": id,
        "product": product
    })
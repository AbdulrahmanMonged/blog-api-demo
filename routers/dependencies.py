from fastapi import APIRouter, Depends, Request


router = APIRouter(prefix="/dependency", tags=["dependency"])


def get_query_params(request: Request, sep: str = "==="):
    converted_query_params = [
        f"{key} {sep} {value}" for key, value in request.query_params.items()
    ]
    return converted_query_params

def get_headers(request: Request, sep: str = "===", qparams = Depends(get_query_params)):
    converted_headers = [
        f"{key} {sep} {value}" for key, value in request.headers.items()
    ]
    return {
        "headers": converted_headers,
        "query_params": qparams,
    }


@router.get("/")
async def main_endpoint(sep: str, converted_headers=Depends(get_headers)):
    return {"items": ["a", "b", "c"], "headers": converted_headers}


@router.get("/new")
async def new_endpoint(converted_headers=Depends(get_headers)):
    return {"items": ["a", "b", "c"], "headers": converted_headers}

class User:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email
    
    
@router.get('/user')
async def test_user(name: str, password: str, email: str, user_dependency: User = Depends(User)):
    return {
        "name": user_dependency.name,
        "email": user_dependency.email
    }
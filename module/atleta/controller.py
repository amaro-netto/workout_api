from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_atletas():
    return {"message": "Lista de atletas"}
from fastapi import APIRouter

router = APIRouter()


@router.get("/alive")
async def alive():
    return {"message": "alive"}

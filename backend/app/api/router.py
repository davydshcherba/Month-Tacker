from fastapi import APIRouter
from app.api.v1.user import user_router
router = APIRouter(prefix="/v1")


@router.get("/health", status_code=200)
async def health():
    return {"status": "OK"}

router.include_router(router=user_router, tags=["User"])
from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["health"])


@router.get("")
def health():
    """Verifica se a API está no ar."""
    return {"status": "ok"}
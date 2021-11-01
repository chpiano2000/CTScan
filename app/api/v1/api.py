from fastapi import APIRouter

from .endpoints.user import router as user_router
# from .endpoints.images import router as images_router
from .endpoints.authentication import router as auth_router
from .endpoints.patient import router as patient_router

router = APIRouter()
router.include_router(auth_router)
router.include_router(user_router)
# router.include_router(images_router)
router.include_router(patient_router)
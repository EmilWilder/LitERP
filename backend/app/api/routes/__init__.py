from fastapi import APIRouter
from .auth import router as auth_router
from .users import router as users_router
from .hr import router as hr_router
from .projects import router as projects_router
from .crm import router as crm_router
from .accounting import router as accounting_router
from .equipment import router as equipment_router
from .production import router as production_router
from .dashboard import router as dashboard_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users_router, prefix="/users", tags=["Users"])
api_router.include_router(hr_router, prefix="/hr", tags=["HR"])
api_router.include_router(projects_router, prefix="/projects", tags=["Projects"])
api_router.include_router(crm_router, prefix="/crm", tags=["CRM"])
api_router.include_router(accounting_router, prefix="/accounting", tags=["Accounting"])
api_router.include_router(equipment_router, prefix="/equipment", tags=["Equipment"])
api_router.include_router(production_router, prefix="/production", tags=["Production"])
api_router.include_router(dashboard_router, prefix="/dashboard", tags=["Dashboard"])

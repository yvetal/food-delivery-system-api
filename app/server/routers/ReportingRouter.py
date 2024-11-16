import logging

logger = logging.getLogger(__name__)

from fastapi import APIRouter, HTTPException, Depends

from server.services.ReportingService import reporting_service
from server.hash import role_required

router = APIRouter()

@router.post(
    "/",
    responses={
        200: {"description": "Successful Response", "model": str},
    })
@router.get("/")
async def get_report(current_user: dict = Depends(role_required("ADMIN"))):
    reports = await reporting_service.get_report()
    return reports


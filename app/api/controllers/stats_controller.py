from typing import List
from fastapi import APIRouter, Depends, status

from app.dto.stats_dto import StatsDTO, StatsFilterDTO
from app.auth.deps import get_admin
from app.api.deps import get_stats_service

from app.services.stats_service import StatsService


class StatsController:
    router = APIRouter(prefix="/stats")

    @router.get(
        "",
        response_model=StatsDTO,
        summary="Get stats",
        description="Retrieve a list of stats.",
        response_description="A list of stats.",
    )
    async def get_stats(
        filter: StatsFilterDTO = Depends(StatsFilterDTO.from_query_params),
        admin: str = Depends(get_admin),
        stats_service: StatsService = Depends(get_stats_service),
    ) -> StatsDTO:
        return await stats_service.get_stats(filter=filter)

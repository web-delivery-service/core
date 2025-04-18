from datetime import datetime
from typing import List, Optional

from fastapi import Query
from app.dto.base_dto import CreateDTO, BaseDTO


class StatsDTO(CreateDTO):
    order_quantity: int
    total_cost: int

    product_quantity: int
    category_quantity: int

    categories_stats: dict[str, int] # dict[category, quantity]


class StatsFilterDTO(CreateDTO):
    start_date: datetime | None
    end_date: datetime | None

    @classmethod
    def from_query_params(
        cls,
        startDate: Optional[str] = Query(None, example="2025-04-01"),
        endDate: Optional[str] = Query(None, example="2025-04-30")
    ):
        def parse_date(date_str):
            return datetime.strptime(date_str, "%Y-%m-%d") if date_str else None
            
        return cls(
            start_date=parse_date(startDate),
            end_date=parse_date(endDate)
        )

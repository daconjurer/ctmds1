from typing import Sequence

from pydantic import BaseModel


class Price(BaseModel):
    price: float
    timestamp: str


class PriceCollection(BaseModel):
    prices: Sequence[Price]

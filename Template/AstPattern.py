from dataclasses import dataclass
from typing import Any

@dataclass
class ItemFilter:
    FilterByType:str
    FilterByName:str
    FilterByValue:Any
    FilterByANID:bytes
    pass

@dataclass
class PatternItem:
    Name:str
    ItemFilters:list[ItemFilter]
    Optional:bool
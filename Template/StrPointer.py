from dataclasses import dataclass

@dataclass
class Pointer:
    """
        Metin üzerinde konum gösteren bir işaretçi
        x -> satır
        y -> sütun
        raw -> index
    """
    x:int = 1
    y:int = 1
    raw:int = 0
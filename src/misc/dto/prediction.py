from dataclasses import dataclass

from datetime import datetime


@dataclass
class PredictionParams:
    conf: float = 0.25
    iou: float = 0.7
    imgsz: int = 640
    max_det: int = 300
    classes: list[int] = None
    line_width: int | None = None


@dataclass
class PredictionDTO:
    params: PredictionParams
    file: bytes = None
    url: str = None


@dataclass
class PredictionResultDTO:
    file_type: str
    source_file_size: str
    result_file_size: str


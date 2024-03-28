import json
import io

from fastapi import APIRouter, Depends, Response
from starlette.responses import StreamingResponse

from src.di.stub import Stub
from src.services.db.db_commands import DBCommands
from src.misc.dto.prediction import PredictionDTO, PredictionResultDTO
from src.misc.dto.users import UserDTO
from src.misc.dto.requests import CreateRequestDTO
from src.services.predictor import Predictor
from src.di.auth import authorize
from src.exceptions.classes.common import MissingRequiredParameterException
import src.exceptions.classes as exceptions

api_router = APIRouter()


def iterator(bytes_string: bytes) -> bytes:
    return io.BytesIO(bytes_string)


@api_router.post('/predict', status_code=201)
async def predict_route(prediction_info: PredictionDTO, user_id: int = Depends(authorize),
                        db: DBCommands = Depends(Stub(DBCommands)),
                        predictor: Predictor = Depends(Stub(Predictor))) -> Response | StreamingResponse:
    if not prediction_info.file and not prediction_info.url:
        raise MissingRequiredParameterException

    user_dto = UserDTO(id=user_id)
    user = await db.get_or_create_user(user_dto)
    if not user.balance >= 1:
        raise exceptions.UserBalanceIsTooLowException

    predict_file, predict_file_info = await predictor.predict(prediction_dto=prediction_info)
    predict_file: bytes
    predict_file_info: PredictionResultDTO

    await db.update_user(user_id=user_id, balance=user.balance - 1)

    request_dto = CreateRequestDTO(user_id=user_id, source_file_size=predict_file_info.source_file_size,
                                   result_file_size=predict_file_info.result_file_size)
    await db.create_request(request_dto)

    json_predict_file_info = json.dumps(predict_file_info.__dict__)
    if predict_file_info.file_type == 'image':
        return Response(content=predict_file, headers={'X-JSON-Data': json_predict_file_info}, media_type="image/png")
    elif predict_file_info.file_type == 'video':
        return StreamingResponse(content=iterator(predict_file), headers={'X-JSON-Data': json_predict_file_info}, media_type="video/mp4")

import imageio
import requests
import numpy as np
from PIL import Image
import cv2
import io
import sys

from ultralytics import YOLO

from src.misc.dto.prediction import PredictionDTO, PredictionResultDTO


class Predictor:
    def __init__(self, model: YOLO):
        self.model = model

    async def predict(self, prediction_dto: PredictionDTO):
        if prediction_dto.file:
            source = prediction_dto.file
            source_file_size = self._convert_bytes_to_kilobytes(source)
        elif prediction_dto.url:
            source = prediction_dto.url
            source_file_size = self.get_file_size_from_url(source)
        else:
            return None

        predict_result = self.model.predict(source, **prediction_dto.params.__dict__)

        if len(predict_result) > 1:
            media_result = self.convert_arrays_to_video(predict_result)
            file_type = 'video'
        else:
            predict_array = predict_result[0].plot()
            media_result = self.convert_array_to_image(predict_array)
            file_type = 'image'

        return media_result, PredictionResultDTO(file_type=file_type, source_file_size=source_file_size,
                                                 result_file_size=self._convert_bytes_to_kilobytes(media_result))

    @staticmethod
    def _convert_bytes_to_kilobytes(file: bytes) -> float:
        kilobytes = sys.getsizeof(file) // 1000
        return kilobytes

    def get_file_size_from_url(self, url: str) -> float:
        try:
            response = requests.head(url)
            file_size_in_bytes = int(response.headers.get('Content-Length', 0))
            return self._convert_bytes_to_kilobytes(file_size_in_bytes)
        except requests.exceptions.RequestException:
            return 0

    @staticmethod
    def convert_array_to_image(array: np.ndarray):
        colored_array = np.uint8(cv2.cvtColor(array, cv2.COLOR_BGR2RGB))
        result_img = Image.fromarray(colored_array)

        io_image = io.BytesIO()
        result_img.save(io_image, format='PNG')
        return io_image.getvalue()

    @staticmethod
    def convert_arrays_to_video(array_list: list[np.array]):
        video = io.BytesIO()
        writer = imageio.get_writer(video, format='avi', fps=30)

        for array in array_list:
            colored_array = np.uint8(cv2.cvtColor(array.plot(), cv2.COLOR_BGR2RGB))
            writer.append_data(colored_array)

        writer.close()
        return video.getvalue()


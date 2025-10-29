from abc import abstractmethod
from io import BufferedReader
from PIL import Image, ImageDraw
from dotenv import load_dotenv
from uuid import uuid4
from os import environ
from typing import List, Self, TypedDict

from azure.core.credentials import AzureKeyCredential
from azure.ai.vision.face import FaceClient
from azure.ai.vision.face.models import (
    FaceAttributeTypeDetection01,
    FaceAttributeTypeDetection03,
    FaceDetectionModel,
    FaceRecognitionModel,
)


class FaceRectangle(TypedDict):
    top: int
    left: int
    width: int
    height: int


class HeadPose(TypedDict):
    pitch: float
    roll: float
    yaw: float


class Occlusion(TypedDict):
    foreheadOccluded: bool
    eyeOccluded: bool
    mouthOccluded: bool


class FaceAttributes(TypedDict):
    headPose: HeadPose
    glasses: str
    occlusion: Occlusion


class DetectionResult(TypedDict):
    faceRectangle: FaceRectangle
    faceAttributes: FaceAttributes


def generate_labelled_image(
    original_image: BufferedReader,
    data: List[DetectionResult],
    output=f"{uuid4()}.png",
    directory=None,
) -> str:
    if directory is None:
        raise ValueError("directory cannot be None")
    image = Image.open(original_image)
    draw = ImageDraw.Draw(image)
    for person_data in data:
        top_left_x, top_left_y = (
            person_data["faceRectangle"]["left"],
            person_data["faceRectangle"]["top"],
        )

        stride_x, stride_y = (
            person_data["faceRectangle"]["width"],
            person_data["faceRectangle"]["height"],
        )
        draw.rectangle(
            (top_left_x, top_left_y, top_left_x + stride_x, top_left_y + stride_y),
            outline=(255, 0, 0, 255),
        )
        # draw.text(
        #     (0, 0),
        #     f"Frente Totalmente Visible? {person_data['faceAttributes']['occlusion']['foreheadOccluded']}\n"
        #     f"Ojos Totalmente Visibles? {person_data['faceAttributes']['occlusion']['eyeOccluded']}\n"
        #     f"Boca Totalmente Visible? {person_data['faceAttributes']['occlusion']['mouthOccluded']}",
        # )

    image.save(f"{directory}/{output}")
    return output


if __name__ == "__main__":
    load_dotenv()

    id = environ["PERSON_GROUP_ID"]
    PERSON_GROUP_ID = id if id != "" else str(uuid4())
    print("Group ID:", PERSON_GROUP_ID)
    with FaceClient(endpoint=ENDPOINT, credential=AzureKeyCredential(API_KEY)) as face_client:
        with open("./zeta_boca_tapada.png", "rb") as image:
            detected_faces: List[DetectionResult] = face_client.detect(
                image.read(-1),
                detection_model=FaceDetectionModel.DETECTION03,
                recognition_model=FaceRecognitionModel.RECOGNITION04,
                return_face_id=False,
                return_face_attributes=[
                    FaceAttributeTypeDetection03.HEAD_POSE,
                    FaceAttributeTypeDetection01.GLASSES,
                    FaceAttributeTypeDetection01.OCCLUSION,
                ],
            )  # type:ignore
            print("generated =", generate_labelled_image(image, detected_faces))

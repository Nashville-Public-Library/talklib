from typing import Type

from pydantic import BaseModel, Field

from talklib.ev import EV
from talklib.notify import Notify
from talklib.ffmpeg import FFMPEG

class TLPod(BaseModel):
    show: str = Field(default=None)
    show_filename: str = Field(default=None)
    bucket_folder: str = Field(default=None)
    notifications: Type[Notify] = Notify()
    ffmpeg: Type[FFMPEG] = FFMPEG()
    ev: Type[EV] = EV()
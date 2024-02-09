import soundcard as sc
import logging
import numpy as np
from typing import Any, Optional

class SoundRecorder:
    """ Sound recorder class """
    SAMPLE_RATE = 16000
    BUF_LEN_SEC = 60
    CHUNK_SIZE_SEC = 0.5
    CHUNK_SIZE = int(SAMPLE_RATE*CHUNK_SIZE_SEC)

    def __init__(self):
        self.data_buf: np.array = None
        self.chunks_num = 0

    def get_microphone(self):
        """ Get adefault microphone """
        mic = sc.default_microphone()
        logging.debug(f"Recording device: {mic}")
        return mic.recorder(samplerate=SoundRecorder.SAMPLE_RATE)

    def record_chunk(self, mic: Any) -> np.array:
        """ Record a new chunk of data """
        return mic.record(numframes=SoundRecorder.CHUNK_SIZE)

    def start_recording(self, chunk_data: np.array):
        """ Start recording a new phrase """
        self.chunks_num = 0
        self.data_buf = np.zeros(SoundRecorder.SAMPLE_RATE * SoundRecorder.BUF_LEN_SEC, dtype=np.float32)
        self._add_to_buffer(chunk_data)

    def continue_recording(self, chunk_data: np.array):
        """ Continue recording a phrase """
        self.chunks_num += 1
        self._add_to_buffer(chunk_data)

    def get_audio_buffer(self) -> Optional[np.array]:
        """ Get audio buffer """
        if self.chunks_num > 0:
            logging.debug(f"Audio length: {self.chunks_num*SoundRecorder.CHUNK_SIZE_SEC}s")
            return self.data_buf[:self.chunks_num*SoundRecorder.CHUNK_SIZE]
        return None

    def _add_to_buffer(self, chunk_data: np.array):
        """ Add new data to the buffer """
        ind_start = self.chunks_num*SoundRecorder.CHUNK_SIZE
        ind_end = (self.chunks_num + 1)*SoundRecorder.CHUNK_SIZE
        self.data_buf[ind_start:ind_end] = chunk_data.reshape(-1)
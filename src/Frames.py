"""Frames.py"""
from src.file_helper import load_audio
import numpy


class Frames:
    def __init__(self, filename, offset):
        self.__filename = filename
        self.__offset = offset
        self.__audio, self.__sampling_rate = load_audio(filename)
        self.__length = int(len(self.__audio) / self.__sampling_rate)
        self.__db = [-100] * self.__offset
        padding = self.__sampling_rate * self.__offset
        borders = numpy.zeros(padding, dtype=numpy.float32)
        fill = numpy.zeros(self.__sampling_rate - (len(self.__audio) % self.__sampling_rate), dtype=numpy.float32)
        self.__audio = numpy.concatenate([borders, audio, fill, borders])

    def browse(self, tv):
        response = []
        while self.__has_next():
            self.__update(tv)
            out.append(self.__output(tv.file_id))
        return response

    def __has_next(self):
        return (self.__iterator + 11) != self.__length

    def __update(self, tv):
        self.__iterator += 1

        mfcc = librosa.feature.mfcc(y=self.__audio[self.__iterator * self.__sampling_rate:(self.__iterator + 10) * self.__sampling_rate], sr=self.__sampling_rate, n_mfcc=80)
        self.__mfcc = numpy.round(numpy.mean(mfcc.T, axis=0), 4)

        db = librosa.core.amplitude_to_db(self.__audio[(self.__iterator + 9) * self.__sampling_rate:(self.__iterator + 10) * self.__sampling_rate])
        self.__db.pop(0)
        self.__db.append(numpy.round(numpy.mean(db), 4))

        for _, row in tv.iterrows():
            if row.timestamps <= self.__iterator:
                self.__pub = row.IsAPub

    def output(self, file_id):
        temp = [self.__pub, file_id.iloc[0], self.__iterator]
        temp = numpy.concatenate([temp, self.__mfcc])
        temp = numpy.concatenate([temps, self.__db])
        return temp
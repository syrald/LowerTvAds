"""file_helper.py"""
import librosa


def load_audio(filename):
    """
    Load an audio file.

    Args:
        filename (str) : file to load.
    
    Returns:

    """
    audio, sampling_rate = librosa.load(filename, sr=44100, res_type="kaiser_fast")
    return audio, sampling_rate
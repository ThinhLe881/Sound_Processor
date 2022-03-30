import pyaudio
import wave
import audioop

def play_normal(file, factor):
    CHUNK = 1024

    wf = wave.open(file, 'rb')
    sampwidth = wf.getsampwidth()

    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(sampwidth),
                    channels=wf.getnchannels(), rate=wf.getframerate(), output=True)

    data = wf.readframes(CHUNK)
    while len(data) > 0:
        stream.write(audioop.mul(data, sampwidth, factor))
        data = wf.readframes(CHUNK)
        
    stream.stop_stream()
    stream.close()
    p.terminate()
import pyaudio
import wave
import audioop


def play_reverse(file, factor):
    CHUNK = 1024

    wf = wave.open(file, 'rb')
    sampwidth = wf.getsampwidth()

    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(sampwidth),
                    channels=wf.getnchannels(), rate=wf.getframerate(), output=True)

    frames = []
    data = wf.readframes(CHUNK)
    while data:    
        frames.append(data)
        data = wf.readframes(CHUNK)

    data = b''.join(frames[::-1])
    
    for i in range(0, len(data), CHUNK):
        stream.write(audioop.mul(data[i:i+CHUNK], sampwidth, factor))
    
    stream.stop_stream()
    stream.close()
    p.terminate()
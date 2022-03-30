import pyaudio
import wave
import audioop

def record(file, length):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    RECORD_SECONDS = int(length)

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    print("--recording--")

    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)): # (rate/chunk): how many chunks needed for 1 sec
        data = stream.read(CHUNK)
        frames.append(data)

    print("--stop recording--")

    stream.stop_stream()
    stream.close()
    p.terminate()
    
    wf = wave.open(file, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
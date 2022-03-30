import pyaudio
import wave
import audioop

def play_left_right(file, channel, factor):
    CHUNK = 1024

    wf = wave.open(file, 'rb')
    sampwidth = wf.getsampwidth()

    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(sampwidth),
                    channels=wf.getnchannels(), rate=wf.getframerate(), output=True)

    data = bytearray(wf.readframes(CHUNK))
    while len(data) > 0:
        # remove left|right channel
        for i in range(0, len(data)):
            if channel == 'R':
                if i % (sampwidth*2) < sampwidth:   # remove left channel
                    data[i] = 0
            else:
                if i % (sampwidth*2) >= sampwidth:  # remove right channel
                    data[i] = 0

        stream.write(audioop.mul(data, sampwidth, factor))
        data = bytearray(wf.readframes(CHUNK))
    
    stream.stop_stream()
    stream.close()
    p.terminate()
import os.path
import pyaudio
import wave
import audioop


CHUNK = 1024
CHANNELS = 2
RATE = 44100
FORMAT = pyaudio.paInt16


def record(file, length):
    record_seconds = int(length)
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                    input=True, frames_per_buffer=CHUNK)
    print("--recording--")
    frames = []

    # (rate/chunk): how many chunks needed for 1 sec
    for i in range(0, int(RATE / CHUNK * record_seconds)):
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


def play_normal(file, factor):
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


def play_left_right(file, channel, factor):
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


def play_reverse(file, factor):
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


def main():
    #------------Menu------------
    print("\n--Sound Processor--")
    quit = True

    while quit:
        print("\n1. Record")
        print("2. Play")
        print("3. Exit")
        opt = input("Option?: ")

        match opt:
            case "1":
                file = input("File name(.wav): ")
                file = file + ".wav"
                check = True

                while (check):
                    length = input("Length(in sec): ")

                    if length.isnumeric():
                        record(file, length)
                        check = False
                    else:
                        print("Invalid input. Try again")

                print("--Done--")
                break;
            case "2":
                volume = 50
                factor = (volume / 100) * 2
                file = input("File name(.wav): ")
                file = file + ".wav"

                if not os.path.isfile(file):
                    print("File not exist")
                else:
                    quit2 = True

                    while quit2:
                        print("\n1. Adjust Volume")
                        print("2. Normal")
                        print("3. Left-Right Panning")
                        print("4. Reverse")
                        print("5. Back")
                        opt2 = input("Option?: ")

                        match opt2:
                            case "1":
                                print("Volume: " + str(volume))
                                check = True

                                while check:
                                    new_volume = input("New volume(0-100): ")
                                    
                                    if new_volume.isnumeric() and 0 <= int(new_volume) <= 100:
                                        volume = int(new_volume)
                                        factor = (volume / 100) * 2
                                        print("Volume: " + str(volume))
                                        play_normal(file, factor)
                                        check = False
                                    else:
                                        print("Invalid input. Try again")
                                print("--Done--")
                                break
                            case "2":
                                play_normal(file, factor)
                                print("--Done--")
                            case "3":
                                check = True

                                while check:
                                    channel = input("Left or Right side louder?(L|R): ")
                                    channel = channel.upper()

                                    if channel == "L" or channel == "R":
                                        play_left_right(file, channel, factor)
                                        check = False
                                    else:
                                        print("Invalid input. Try again")

                                print("--Done--")
                                break
                            case "4":
                                play_reverse(file, factor)
                                print("--Done--")
                            case "5":
                                quit2 = False
                                break
                            case _:
                                print("Invalid option. Try again")
                                break
                break
            case "3":
                print("--Exit--")
                quit = False
                break
            case _:
                print("Invalid option. Try again")
                break


if __name__ == '__main__':
    main()

import os.path

from src.record import record
from src.normal import play_normal
from src.left_right import play_left_right
from src.reverse import play_reverse

def main():
    #------------Menu------------
    print("\n--Sound Processor--")

    quit = True
    while quit:
        print("\n1. Record")
        print("2. Play")
        print("3. Exit")
        opt = input("Option?: ")

        if opt == "1":
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

        elif opt == "2":
            volume = 50
            factor = (volume / 100) * 2
            file = input("File name(.wav): ")
            file = file + ".wav"
            if os.path.isfile(file):
                quit2 = True
                while quit2:
                    print("\n1. Adjust Volume")
                    print("2. Normal")
                    print("3. Left-Right Panning")
                    print("4. Reverse")
                    print("5. Back")
                    opt2 = input("Option?: ")

                    if opt2 == "1":
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

                    elif opt2 == "2":
                        play_normal(file, factor)
                        print("--Done--")

                    elif opt2 == "3":
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

                    elif opt2 == "4":
                        play_reverse(file, factor)
                        print("--Done--")

                    elif opt2 == "5":
                        quit2 = False

                    else:
                        print("Invalid option. Try again")
            else:
                print("File not exist")

        elif opt == "3":
            print("--Exit--")
            quit = False
            
        else:
            print("Invalid option. Try again")

if __name__ == '__main__':
    main()

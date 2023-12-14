import wave  # wav header
import pyaudio  # register sound with a microphone
import sounddevice as sd  # play wav
import numpy as np  # play wav
import pyglet

pyglet.options['audio'] = ('directsound', 'silent', 'openal', 'pulse', 'xaudio2')

import pyglet.media  # DirectSound


def play_wav(file_path):
    # Read the WAV file
    with wave.open(file_path, 'rb') as wav_file:
        # Get audio data
        frames = wav_file.readframes(wav_file.getnframes())
        audio_data = np.frombuffer(frames, dtype=np.int16)

        # Play the audio
        sd.play(audio_data, wav_file.getframerate())
        sd.wait()


def play_DirectSound(file_path):
    audio_file = pyglet.media.load(file_path)  # Replace with the path to your audio file

    # Create a media player
    player = pyglet.media.Player()
    player.queue(audio_file)

    # Play the audio
    player.play()

    # Keep the program running to allow audio playback
    pyglet.app.run()


def display_wav_header(file_path):
    with wave.open(file_path, 'rb') as wav_file:
        print("WAV File Header:")
        print("Format: {}".format(wav_file.getparams()))
        print("Channels: {}".format(wav_file.getnchannels()))
        print("Sample Width: {} bytes".format(wav_file.getsampwidth()))
        print("Frame Rate: {} Hz".format(wav_file.getframerate()))
        print("Number of Frames: {}".format(wav_file.getnframes()))
        print("Compression Type: {}".format(wav_file.getcompname()))


def register_sound_microphone(record_time_seconds, file_name, selected_format, selected_num_of_channels, selected_rate,
                              selected_frames_per_buffer):
    paudio = pyaudio.PyAudio()

    stream = paudio.open(

        format=selected_format,
        channels=selected_num_of_channels,
        rate=selected_rate,
        input=True,
        frames_per_buffer=selected_frames_per_buffer

    )

    print("Start of the recording")

    frames = []
    for i in range(0, int(selected_rate / selected_frames_per_buffer * record_time_seconds)):
        data = stream.read(selected_frames_per_buffer)
        frames.append(data)

    print("End of recording")

    stream.stop_stream()
    stream.close()
    paudio.terminate()

    wav_object = wave.open(file_name, 'wb')
    wav_object.setnchannels(selected_num_of_channels)
    wav_object.setsampwidth(paudio.get_sample_size(selected_format))
    wav_object.setframerate(selected_rate)
    wav_object.writeframes(b"".join(frames))
    wav_object.close()


def display_menu():
    print("===== Sound Processing Menu =====")
    print("1. Play WAV File")
    print("2. Display WAV Header")
    print("3. Record from Microphone")
    print("4. Exit")
    print("===============================")

    while True:
        choice = input("Enter your choice (1-4): ")

        if choice == "1":
            file_in_name = input("Enter input audio file name: ")
            play_wav(file_in_name)
        elif choice == "2":
            file_in_name = input("Enter input audio file name: ")
            display_wav_header(file_in_name)
        elif choice == "3":
            selected_record_time_s = float(input("Enter recording time in seconds: "))
            selected_file_out_name = input("Enter output file name: ")
            selected_file_format = pyaudio.paInt16
            selected_num_of_channels = int(input("Enter number of channels: "))
            selected_rate = int(input("Enter sample rate: "))
            selected_frames_per_buffer = int(input("Enter frames per buffer: "))
            register_sound_microphone(selected_record_time_s, selected_file_out_name, selected_file_format,
                                      selected_num_of_channels, selected_rate, selected_frames_per_buffer)
        elif choice == "4":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")


if __name__ == "__main__":
    '''
    record_time_s = 5
    file_out_name = "out.wav"
    file_format = pyaudio.paInt16
    num_of_channels = 1
    rate = 16000
    frames_per_buffer = 3200
    file_in_name = "./atw.wav"
    x = "C:\\Users\\1312\\PycharmProjects\\Sound_card\\atw.wav"
    '''
    # display_menu()
    play_DirectSound("atw.wav")

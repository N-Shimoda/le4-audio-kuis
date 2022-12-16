import simpleaudio

wav_obj = simpleaudio.WaveObject.from_wave_file("sound/doppler_trim.wav")
play_obj = wav_obj.play()
play_obj.wait_done()

if play_obj.is_playing():
    print("still playing")
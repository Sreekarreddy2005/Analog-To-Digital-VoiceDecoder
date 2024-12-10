import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
import soundfile as sf
import speech_recognition as sr

# Recording parameters
sampling_rate = 44100  # Hz

# Create a buffer to store the recorded audio
audio_buffer = []

# Define a callback function to capture audio chunks
def audio_callback(indata, frames, time, status):
    audio_buffer.append(indata.copy())

# Start recording
print("Recording... Press Enter to stop.")
stream = sd.InputStream(callback=audio_callback, channels=1, samplerate=sampling_rate, dtype='float32')
with stream:
    input()  # Wait until the user presses Enter

print("Recording finished")

# Concatenate all chunks to form the full audio signal
audio = np.concatenate(audio_buffer, axis=0)

# Normalize the audio signal between -1 and 1
audio = audio / np.max(np.abs(audio))

# Save the recorded audio to a WAV file
sf.write('recorded_audio.wav', audio, sampling_rate)

# Time axis for plotting
time = np.linspace(0, len(audio) / sampling_rate, len(audio))

# Plotting the original analog signal with time on the x-axis
plt.figure(figsize=(10, 4))
plt.plot(time, audio)
plt.title("Analog Signal")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.grid()
plt.show()

# Filtering to remove noise
b, a = signal.butter(4, 0.1, 'low')  # Low-pass filter
filtered_audio = signal.filtfilt(b, a, audio, axis=0)

# Plotting the filtered analog signal
plt.figure(figsize=(10, 4))
plt.plot(time, filtered_audio)
plt.title("Filtered Analog Signal")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.grid()
plt.show()

# Playback the filtered (noise-reduced) audio
print("Playing back the noise-reduced audio...")
sd.play(filtered_audio, samplerate=sampling_rate)
sd.wait()  # Wait until playback is finished

# Quantization
def quantize(signal, num_levels):
    min_val, max_val = min(signal), max(signal)
    step_size = (max_val - min_val) / num_levels
    quantized_signal = np.round(signal / step_size) * step_size
    return quantized_signal 

def non_uniform_quantize(signal, num_levels):
    signal_magnitude = np.log1p(np.abs(signal))
    quantized_signal_magnitude = quantize(signal_magnitude, num_levels)
    return np.sign(signal) * np.expm1(quantized_signal_magnitude)

num_levels = 256
uniform_digital_signal = quantize(filtered_audio, num_levels)
non_uniform_digital_signal = non_uniform_quantize(filtered_audio, num_levels)

# Plotting the uniform quantized digital signal
plt.figure(figsize=(10, 4))
plt.plot(time, uniform_digital_signal, 'r')
plt.title("Uniform Quantized Digital Signal")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.grid()
plt.show()

# Plotting the non-uniform quantized digital signal
plt.figure(figsize=(10, 4))
plt.plot(time, non_uniform_digital_signal, 'g')
plt.title("Non-uniform Quantized Digital Signal")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.grid()
plt.show()

# Playback the uniform quantized digital signal
print("Playing back the uniform quantized digital audio...")
sd.play(uniform_digital_signal, samplerate=sampling_rate)
sd.wait()  # Wait until playback is finished

print("Playing back the non-uniform quantized digital audio...")
sd.play(non_uniform_digital_signal, samplerate=sampling_rate)
sd.wait()  # Wait until playback is finished

# Transcribe the recorded audio using speech recognition
recognizer = sr.Recognizer()
with sr.AudioFile("recorded_audio.wav") as source:
    audio_data = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio_data)
        print("Transcription: " + text)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

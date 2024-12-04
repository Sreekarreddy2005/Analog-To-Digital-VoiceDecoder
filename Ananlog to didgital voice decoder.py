import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt

# Recording parameters
duration = 5  # seconds
sampling_rate = 44100  # Hz

# Record audio
print("Recording...")
audio = sd.rec(int(duration * sampling_rate), samplerate=sampling_rate, channels=1, dtype='float64')
sd.wait()  # Wait until the recording is finished
print("Recording finished")

# Plotting the original analog signal
plt.figure(figsize=(10, 4))
plt.plot(audio)
plt.title("Analog Signal")
plt.xlabel("Sample Number")
plt.ylabel("Amplitude")
plt.grid()
plt.show()

# Quantization
def quantize(signal, num_levels):
    min_val, max_val = min(signal), max(signal)
    step_size = (max_val - min_val) / num_levels
    quantized_signal = np.round(signal / step_size) * step_size
    return quantized_signal

num_levels = 256  # Example: 8-bit quantization
digital_signal = quantize(audio, num_levels)

# Plotting the quantized digital signal
plt.figure(figsize=(10, 4))
plt.plot(digital_signal, 'r')
plt.title("Digital Signal (Quantized)")
plt.xlabel("Sample Number")
plt.ylabel("Amplitude")
plt.grid()
plt.show()

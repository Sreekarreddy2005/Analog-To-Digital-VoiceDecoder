import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
#signal that has been discretized into a finite set of levels or values, typically for the purpose of digital signal processing or data compression
#A digital signal is a representation of data using discrete values, such as binary digits, or bits
#A continuous electrical signal that varies in frequency and strength over time(eg: human voice)
# Recording parameters
duration = 5  # seconds
sampling_rate = 44100 # Hz

# Record audio
print("Recording...")
audio = sd.rec(int(duration * sampling_rate), samplerate=sampling_rate, channels=1, dtype='float64') 
#sd.rec: Records audio using the specified sampling rate and duration. sd=sonddevice
sd.wait()  # Wait until the recording is finished
print("Recording finished")

# Playback the recorded audio
print("Playing back the recorded audio...")
sd.play(audio, samplerate=sampling_rate)
sd.wait()  # Wait until playback is finished

# Plotting the original analog signal
plt.figure(figsize=(10, 4)) #Creates a new figure for plotting.
plt.plot(audio)#Plots the recorded audio signal.
plt.title("Analog Signal") #Adds a title to the plot
plt.xlabel("Sample Number") #Labels the x-axis.
plt.ylabel("Amplitude") #Labels the y-axis.
plt.grid() #Adds a grid to the plot for better readability.
plt.show() #Displays the plot.

# Quantization
#This function converts the continuous analog signal into discrete digital levels.
def quantize(signal, num_levels):
    min_val, max_val = min(signal), max(signal)#Find the minimum and maximum values of the signal.
    step_size = (max_val - min_val) / num_levels #Calculate the step size based on the number of quantization levels.
    quantized_signal = np.round(signal / step_size) * step_size #Quantize the signal by rounding it to the nearest step size.
    return quantized_signal 

num_levels = 256 
#Number of quantization levels (256 levels for 8-bit quantization).
digital_signal = quantize(audio, num_levels)
#The quantized version of the recorded audio signal.

# Plotting the quantized digital signal
plt.figure(figsize=(10, 4))
#It takes a tuple (width, height) where:
#width is the width of the figure.
#height is the height of the figure.
plt.plot(digital_signal, 'r')
plt.title("Digital Signal (Quantized)")
plt.xlabel("Sample Number")
plt.ylabel("Amplitude")
plt.grid()
plt.show()

# Playback the quantized digital signal
print("Playing back the quantized digital audio...")
sd.play(digital_signal, samplerate=sampling_rate)
sd.wait()  # Wait until playback is finished

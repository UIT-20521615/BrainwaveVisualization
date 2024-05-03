import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Generate some sample EEG data
num_samples = 1000
num_channels = 8
eeg_data = np.random.uniform(0, 50, size=(num_samples, num_channels))

# Create subplots for each channel and power plot
fig, axs = plt.subplots(num_channels + 1, 1, figsize=(10, 12), gridspec_kw={'height_ratios': [3]*num_channels + [5]})

# Initialize line objects for each channel
lines = [ax.plot([], [], lw=2)[0] for ax in axs[:-1]]
power_text = axs[-1].text(0.5, 0.5, '', horizontalalignment='center', verticalalignment='center', transform=axs[-1].transAxes, fontsize=16, bbox=dict(facecolor='white', alpha=0.5, edgecolor='black', linewidth=2))

# Add Bluetooth symbol annotation
bluetooth_annotation = fig.text(0.05, 0.95, '🔵 Connected', fontsize=16)

# Set titles and labels
for i, ax in enumerate(axs[:-1]):
    ax.set_title(f'Channel {i+1}')
    ax.set_xlim(0, num_samples)
    ax.set_ylim(0, 60)
    ax.set_ylabel('A (uV)')

# Set labels for power plot
axs[-1].set_title('Detected Frequency Band')
axs[-1].set_xlabel('Time')
axs[-1].set_ylabel('')

# Update function for animation
def update(frame):
    global eeg_data
    global power_text

    # Update EEG data
    for i, line in enumerate(lines):
        if i < num_channels:  # Ensure the loop index doesn't exceed the number of channels
            line.set_data(np.arange(frame), eeg_data[:frame, i])

    # Classify the signal based on average amplitude
    avg_amplitude = np.mean(eeg_data[:frame, :], axis=0)
    max_channel = np.argmax(avg_amplitude)

    # Define frequency band labels
    band_labels = ["Delta", "Theta", "Alpha", "Beta", "Gamma"]

    if np.isnan(avg_amplitude[max_channel]):
        power_text.set_text(f'Detected frequency band: None')
    else:
        if max_channel < len(band_labels):
            bluetooth_annotation.set_text("Bluetooth Connected")  # Change Bluetooth symbol to indicate connection status
            if avg_amplitude[max_channel] >= 1 and avg_amplitude[max_channel] < 4:
                power_text.set_text(f'Detected frequency band: Delta')
            elif avg_amplitude[max_channel] >= 4 and avg_amplitude[max_channel] < 8:
                power_text.set_text(f'Detected frequency band: Theta')
            elif avg_amplitude[max_channel] >= 8 and avg_amplitude[max_channel] < 12:
                power_text.set_text(f'Detected frequency band: Alpha')
            elif avg_amplitude[max_channel] >= 12 and avg_amplitude[max_channel] < 25:
                power_text.set_text(f'Detected frequency band: Beta')
            elif avg_amplitude[max_channel] >= 25 and avg_amplitude[max_channel] <= 30:
                power_text.set_text(f'Detected frequency band: Gamma')


        else:
            power_text.set_text(f'Detected frequency band: None')
            bluetooth_annotation.set_text("Bluetooth Disconnected")  # Change Bluetooth symbol to indicate connection status


    return lines + [power_text]

# Create animation
ani = FuncAnimation(fig, update, frames=num_samples, blit=True)

plt.show()

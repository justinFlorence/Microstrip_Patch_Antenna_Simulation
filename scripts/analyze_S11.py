import pandas as pd
import matplotlib.pyplot as plt

# Load S-parameter data (Adjust the filename and column names as needed)
s_data = pd.read_csv('S11_freq_data.csv')

# Typical exported HFSS CSV files have headers like 'Freq [GHz]' and 'dB(S(1,1))'
freq = s_data['Freq [GHz]']
S11 = s_data['dB(ActiveS(1:1)) []']

# Plot S11 vs Frequency
plt.figure()
plt.plot(freq, S11, marker='o')
plt.title('S11 vs Frequency')
plt.xlabel('Frequency (GHz)')
plt.ylabel('S11 (dB)')
plt.grid(True)
plt.savefig('S11_plot.png', dpi=300)  # Save the plot
plt.show()  # Display the plot

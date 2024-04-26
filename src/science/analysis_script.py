import matplotlib.pyplot as plt
import numpy as np

with open('./src/science/data.txt', 'r') as file:
    data = file.read()
    analysis_data = data.split('\n')

analysis_data = analysis_data[:-1]
print(analysis_data)
analysis_data = [float(i) for i in analysis_data]
analysis_data = [int(i) for i in analysis_data]
analysis_data = analysis_data[2:]


x = range(1, len(analysis_data) + 1)


# Create the plot
plt.figure(figsize=(10, 6))
plt.plot(x, analysis_data, marker='o', linestyle='-', color='b')
plt.title('Analysis Data Plot')
plt.xlabel('Times')
plt.ylabel('Execution Time')
plt.grid(True)
plt.ylim(0, 50)  # Ensure y-axis starts at 0 and has some space above the max value
plt.xticks(np.arange(min(x), max(x)+1, 1.0))


for i, value in enumerate(analysis_data):
    plt.annotate(value, (x[i], analysis_data[i]), textcoords="offset points", xytext=(0,10), ha='center')


# Show the plot
plt.show()

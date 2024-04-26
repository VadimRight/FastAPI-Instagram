import matplotlib.pyplot as plt

with open('./src/science/data.txt', 'r') as file:
    data = file.read()
    analysis_data = data.split('\n')

analysis_data = analysis_data[:-1]
print(analysis_data)
analysis_data = [float(i) for i in analysis_data]

analysis_data = analysis_data[2:]
plt.plot(analysis_data)
plt.show()


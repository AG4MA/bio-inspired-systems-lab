# utils.py

def generate_random_number(min_value, max_value):
    """Generate a random number between min_value and max_value."""
    import random
    return random.uniform(min_value, max_value)

def log_data(data, filename):
    """Log data to a specified file."""
    with open(filename, 'a') as file:
        file.write(f"{data}\n")

def visualize_data(data):
    """Visualize the given data using a simple plot."""
    import matplotlib.pyplot as plt
    plt.plot(data)
    plt.xlabel('Time')
    plt.ylabel('Value')
    plt.title('Quorum Sensing Data Visualization')
    plt.show()
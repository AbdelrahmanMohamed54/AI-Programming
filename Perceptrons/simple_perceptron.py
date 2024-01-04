import numpy as np


class Perceptron:
    def __init__(self, input_size):
        self.weights = np.random.randn(input_size) * 0.0001

    def predict(self, inputs):
        return int(np.dot(inputs, self.weights) > 0)

    def train(self, inputs, target, learning_rate=0.01):
        prediction = self.predict(inputs)
        if target != prediction:
            update = learning_rate * (target - prediction) * inputs
            self.weights += update


def generate_noisy_samples(ideal, num_samples=100, noise_level=1.0):
    data = {key: [] for key in ideal.keys()}

    for digit_key, ideal_digit in ideal.items():
        for _ in range(num_samples):
            new_digit = ideal_digit + np.random.normal(loc=0, scale=noise_level, size=ideal_digit.shape)
            data[digit_key].append(new_digit)

    return data


# Ideals with 5x4 dimensions
ideals = {
    0: np.array([[0, 1, 1, 0],
                 [1, 0, 0, 1],
                 [1, 0, 0, 1],
                 [1, 0, 0, 1],
                 [0, 1, 1, 0]]),

    1: np.array([[0, 0, 1, 0],
                 [0, 1, 1, 0],
                 [0, 0, 1, 0],
                 [0, 0, 1, 0],
                 [0, 0, 1, 0]]),

    2: np.array([[1, 1, 1, 1],
                 [1, 0, 0, 1],
                 [1, 0, 0, 1],
                 [1, 1, 1, 1],
                 [1, 0, 0, 0]]),

    3: np.array([[1, 0, 1, 0],
                 [1, 0, 1, 0],
                 [1, 1, 1, 1],
                 [0, 0, 1, 0],
                 [0, 0, 1, 0]]),

    4: np.array([[0, 1, 1, 1],
                 [0, 0, 0, 1],
                 [0, 1, 1, 1],
                 [0, 0, 0, 1],
                 [0, 0, 0, 1]]),

    5: np.array([[1, 1, 0, 0],
                 [1, 0, 1, 0],
                 [1, 1, 1, 1],
                 [1, 0, 0, 1],
                 [0, 1, 1, 0]]),

    6: np.array([[0, 0, 0, 0],
                 [0, 1, 0, 0],
                 [0, 0, 0, 0],
                 [0, 0, 0, 0],
                 [0, 0, 0, 0]]),

    7: np.array([[0, 0, 0, 0],
                 [0, 1, 0, 0],
                 [0, 0, 0, 0],
                 [0, 0, 0, 0],
                 [0, 0, 0, 0]]),

    8: np.array([[0, 0, 0, 0],
                 [0, 1, 0, 0],
                 [0, 0, 0, 0],
                 [0, 0, 0, 0],
                 [0, 0, 0, 0]]),

    9: np.array([[0, 0, 0, 0],
                 [0, 1, 0, 0],
                 [0, 0, 0, 0],
                 [0, 0, 0, 0],
                 [0, 0, 0, 0]])
}

num_samples_per_digit = 100
noise_level = 1

# Generate a dataset with noisy samples
dataset_with_noise = generate_noisy_samples(ideals, num_samples=num_samples_per_digit, noise_level=noise_level)

# Extract features and labels from the generated dataset
dataset = np.array([sample.flatten() for samples in dataset_with_noise.values() for sample in samples])
labels = np.array([label for label, samples in dataset_with_noise.items() for _ in samples])

# Split the data into training and validation sets (90%-10%)
split_index = int(0.9 * len(dataset))
train_data, val_data = dataset[:split_index], dataset[split_index:]
train_labels, val_labels = labels[:split_index], labels[split_index:]

# Initialize the Perceptron and train it
perceptron = Perceptron(input_size=train_data.shape[1])

# Training the Perceptron with Early Stopping
max_iterations = 1000
best_weights = np.copy(perceptron.weights)
unchanged_iterations = 0
best_val_accuracy = 0

for epoch in range(max_iterations):
    unchanged_weights = np.copy(perceptron.weights)

    for inputs, label in zip(train_data, train_labels):
        target = int(label == 0)
        perceptron.train(inputs, target)

    # Record accuracy on training and validation sets after every 100 updates
    if (epoch + 1) % 100 == 0:
        correct_train_predictions = sum(
            perceptron.predict(inputs) == int(label == 0) for inputs, label in zip(train_data, train_labels))
        train_accuracy = correct_train_predictions / len(train_labels)

        correct_val_predictions = sum(
            perceptron.predict(inputs) == int(label == 0) for inputs, label in zip(val_data, val_labels))
        val_accuracy = correct_val_predictions / len(val_labels)

        print(
            f"Perceptron - Epoch {epoch + 1}: Training Accuracy = {train_accuracy * 100:.2f}%, Validation Accuracy = {val_accuracy * 100:.2f}%")

        # Update best weights if validation accuracy improves
        if val_accuracy > best_val_accuracy:
            best_val_accuracy = val_accuracy
            best_weights = np.copy(perceptron.weights)

        # Check if weights are unchanged
        if np.array_equal(unchanged_weights, perceptron.weights):
            unchanged_iterations += 1
        else:
            unchanged_iterations = 0

        # Break if weights are unchanged for too long
        if unchanged_iterations > 10:
            print(f"Perceptron - Converged after {epoch + 1} iterations.")
            break

# Use the best weights for final evaluation
perceptron.weights = best_weights

# Display final accuracy for the Perceptron
correct_train_predictions = sum(
    perceptron.predict(inputs) == int(label == 0) for inputs, label in zip(train_data, train_labels))
train_accuracy = correct_train_predictions / len(train_labels)
print(f"Perceptron - Training Accuracy = {train_accuracy * 100:.2f}%")

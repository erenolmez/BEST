import numpy as np

# from sklearn.model_selection import train_test_split
# X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size = 0.2, random_state = 1)

# Load the data
feature_fall = np.load('ramil_features_dusus.npy')
feature_nonfall = np.load('ramil_features_no_dusus.npy')

# Create labels for the data
label_fall = np.full(len(feature_fall), 1)
label_nonfall = np.full(len(feature_nonfall), 0)

print(len(feature_fall))
print(len(feature_nonfall))
print(feature_fall)
# Combine the data and labels
features = np.concatenate((feature_fall, feature_nonfall), axis=0)
labels = np.concatenate((label_fall, label_nonfall), axis=0)

# Shuffle the data and labels randomly
permutation = np.random.permutation(features.shape[0])
shuffled_features = features[permutation]
shuffled_labels = labels[permutation]

# Extract 72 fall and 72 nonfall features and combine them
fall_indices = np.where(shuffled_labels == 1)[0][:68]
nonfall_indices = np.where(shuffled_labels == 0)[0][:68]
selected_indices = np.concatenate((fall_indices, nonfall_indices))
selected_features = shuffled_features[selected_indices]
selected_labels = shuffled_labels[selected_indices]
# 69
# 75
# Concatenate the rest of the features and labels
remaining_indices = np.delete(np.arange(shuffled_features.shape[0]), selected_indices)
remaining_features = shuffled_features[remaining_indices]
remaining_labels = shuffled_labels[remaining_indices]

# Concatenate the selected features and labels with the remaining features and labels
features = np.concatenate((selected_features, remaining_features), axis=0)
labels = np.concatenate((selected_labels, remaining_labels), axis=0)

# Save the shuffled and modified data and labels to npy files
np.save('shuffled_features.npy', features)
np.save('shuffled_labels.npy', labels)

# Print the length of the shuffled features and labels
print(len(features))
print(len(labels))

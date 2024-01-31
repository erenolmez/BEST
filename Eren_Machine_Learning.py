#%%
import math as math
from matplotlib import pyplot as plt
import numpy as np
import time
import RPi.GPIO as GPIO
#%%


GPIO.setmode(GPIO.BOARD)
GPIO.setup(21, GPIO.IN)
GPIO.setup(22, GPIO.OUT)
class KNN:
    def __init__(self):
        self.shuffled_features = np.load('shuffled_features.npy')
        self.shuffled_labels = np.load('shuffled_labels.npy')
        
        for i in range(self.shuffled_features.shape[0]):
            self.shuffled_features[i][0] = self.shuffled_features[i][0]*80
        
        print(np.amax(self.shuffled_features, axis=0))
        print(np.amin(self.shuffled_features, axis=0))
        
        # print(len(self.shuffled_features))
        # print(len(self.shuffled_labels))

        self.feature_train = self.shuffled_features[0:136]
        self.feature_test = self.shuffled_features[136:169]

        self.label_train = self.shuffled_labels[0:136]
        self.label_test = self.shuffled_labels[136:169]
        # print(len(label_test))

        # Normalization of the features
        # self.mean = np.mean(self.shuffled_features, axis=0)
        # self.std = np.std(self.shuffled_features, axis=0)
        # shuffled_features = (self.shuffled_features - self.mean) /self.std
        self.normalized_feature_test = self.feature_test
        self.normalized_feature_train = self.feature_train

        # plotting the data
        # for j in range(len(self.feature_train)):
        #     if label_train[j] == 1:
        #         p0 = plt.scatter(self.feature_train[j][0], self.feature_train[j][1], s=2, linewidths=2, color='red', label='fall')
        #     if label_train[j] == 0:
        #         p1 = plt.scatter(self.feature_train[j][0], self.feature_train[j][1], s=2, linewidths=2, color='blue', label='non-fall')
        # plt.legend(handles=[p0, p1], loc='best')

        # plt.figure()
        # ax = plt.axes(projection='3d')
        # for j in range(len(self.shuffled_features)):
        #     if self.shuffled_labels[j] == 1:
        #         p0 = ax.scatter3D(self.shuffled_features[j][0], self.shuffled_features[j][1], self.shuffled_features[j][2], c='r', s=2, label='fall')
        #     if self.shuffled_labels[j] == 0:
        #         p1 = ax.scatter3D(self.shuffled_features[j][0], self.shuffled_features[j][1], self.shuffled_features[j][2], c='b', s=2, label='non-fall')
        # plt.legend(handles=[p0, p1], loc='best')
        # ax.set_xlabel('Energy', labelpad=20)
        # ax.set_ylabel('Frequency', labelpad=20)
        # ax.set_zlabel('Peak', labelpad=20)
        # ax.set_title('3D scatter plot of for the three features')

    def calc_euc_distance(self, data_1, data_2):
        distance = 0
        for j in range(len(self.normalized_feature_train[1])-1):
            distance += (data_1[j] - data_2[j])**2
        return math.sqrt(distance)


    def locate_neighbours(self, data_train, data_test_frag, number):
        potential_neigh = []
        distance_list = list()
        for j in data_train:
            distance_list.append(self.calc_euc_distance(data_test_frag, j))
            potential_neigh.append(j)
        distance_np = np.array(distance_list)
        potential_neigh_np = np.array(potential_neigh)
        neighbour_indexes = distance_np.argsort()
        potential_neigh_np = potential_neigh_np[neighbour_indexes]
        neighbors = potential_neigh_np[:number]
        distance_sorted = np.sort(distance_np)[:number]
        total_distance = distance_sorted.sum()
        weight_factor = []
        for x in distance_sorted:
            if x == 0:
                weight_factor.append(0)
            else:
                weight_factor.append(total_distance / x)
        weight_factor = np.array(weight_factor)
        if weight_factor.sum() == 0:
            weight_factor = weight_factor
        else:
            weight_factor = weight_factor / weight_factor.sum()
        return neighbors, neighbour_indexes, weight_factor


    def predict_classification(self, data_test_frag, number):
        w_sum_labels = np.zeros(2)
        neighbors = self.locate_neighbours(self.normalized_feature_train, data_test_frag, number)
        label_array = []
        for i in range(len(neighbors[0])):
            label_index = neighbors[1][i]
            label_array.append(self.label_train[label_index])
            w_sum_labels[int(self.label_train[label_index])] += neighbors[2][i]
        return float(np.argmax(w_sum_labels)), w_sum_labels


    def find_optimum_K(self):
        success_rates = list()
        for j in range(int(len(self.normalized_feature_train))):
            true_prediction = 0
            for i in range(len(self.normalized_feature_test)):
                prediction = self.predict_classification(self.normalized_feature_test[i], j+1)[0]
                if self.label_test[i] == prediction:
                    true_prediction += 1
            percentage_result = true_prediction/len(self.normalized_feature_test) * 100
            success_rates.append(percentage_result)
        max_success = max(success_rates)
        k_index = success_rates.index(max_success) + 1
        print("Success rate is: " + str(max_success) + " % for K = " + str(k_index))

    def accuracy_test(self):
        true_prediction = 0
        test_number = int(len(self.normalized_feature_test))
        for i in range(test_number):
            prediction = self.predict_classification(self.normalized_feature_test[i], 1)[0]
            if self.label_test[i] == prediction:
                true_prediction += 1
        percentage_result = true_prediction/test_number * 100
        print("Success rate is: " + str(percentage_result))

    def confusion_matrix(self):
        test_number = int(len(self.normalized_feature_test))
        label_predict = np.array([])
        for i in range(test_number):
            prediction = self.predict_classification(self.normalized_feature_test[i], 8)[0]
            label_predict = np.append(label_predict, prediction)

        labels = [0, 1]

        conf_mat = np.zeros((2, 2))
        for i in range(len(label_test)):
            conf_mat[int(label_test[i])][int(label_predict[i])] += 1
        plt.figure()
        plt.imshow(conf_mat, interpolation='nearest', cmap=plt.cm.Blues)
        plt.title('Confusion matrix: Weighted KNN, Ramil')
        plt.colorbar()

        tick_marks = np.arange(len(labels))
        plt.xticks(tick_marks, labels, rotation=90)
        plt.yticks(tick_marks, labels)

        thresh = conf_mat.max() / 2.
        for i, j in np.ndindex(conf_mat.shape):
            plt.text(j, i, conf_mat[i, j], ha='center', va='center',
                    color='white' if conf_mat[i, j] > thresh else 'black')

        # plt.xlabel('Predicted label')
        # plt.ylabel('Actual label')
        plt.show()

    def predicton_based_on_feature_extraction(self, feature_extraction_data):
        feature_extraction_data[0] = feature_extraction_data[0]*80
        # feature_extraction_data = (feature_extraction_data  - self.mean) /self.std
        if self.predict_classification(feature_extraction_data, 1)[0] == 1:
            print("Suspected fall") 
            GPIO.output(22, GPIO.HIGH)
            time.sleep(1)
            GPIO.output(22, GPIO.LOW)
        else:
            print("No fall detected")
            GPIO.output(22, GPIO.LOW)         
               
        # find_optimum_K()

        # accuracy_test()
        # plt.show()
        # confusion_matrix()

        # print(predict_classification(feature_train, self.feature_test[3], 14, label_train)[0])
        # print(label_test[1])
        # print(self.feature_test[1])
        # print(label_test)
        
# %%
Knnobj = KNN()
c = np.array([1,2,3])
time1 = time.time()
a = Knnobj.predict_classification(c,9)
print(a[0])
print(f"elapsed time: {time.time() - time1}")

# %%

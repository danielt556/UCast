import os
from DNN.data_builder import BigCubeDataBuilder
from keras.models import Sequential, model_from_json
from keras.layers import Dense
from keras.utils import np_utils
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error

from core.config import PATH

class Learner:
	def __init__(self, input):
		#####   INITIALIZATION
		#PATH + "/ALL_DAY_CLEANED(231, 624, 800, 24).npz"
		self._data_builder = BigCubeDataBuilder(input)

		#micsorez cubul astfel incat sa antreneze doar pe date din mijlocul imaginii, dar alea care is mai aproape de radar
		#400 am folosit pentru experimentele mele
		#!self._data_builder.crop_cube(400)
		x, y, _ = self._data_builder.next_batch(2)
		self._input_dim = x.shape[1]
		self._output_dim = y.shape[1]

	#Asta e numele dupa care se salveaza si citesc modele de pe disc - Variabila globala importanta de setat
		self._model_name = "model2"

		##### CREATE AND TRAIN MODEL

		# Creating a model - model 2 -> modelul pe care am facut experimentele si de pe care sunt rezultatele
		self._model = Sequential()
		self._model.add(Dense(2000, input_dim=self._input_dim, activation='relu'))
		self._model.add(Dense(1000, activation='relu'))
		self._model.add(Dense(2000, activation='relu'))
		self._model.add(Dense(1000, activation='relu'))
		self._model.add(Dense(500, activation='relu'))
		self._model.add(Dense(1000, activation='relu'))
		self._model.add(Dense(500, activation='relu'))
		self._model.add(Dense(1000, activation='relu'))
		self._model.add(Dense(200, activation='relu'))

		self._model.add(Dense(self._output_dim, activation='linear'))

		# Compiling model
		self._model.compile(loss='mean_squared_error', optimizer='adam', metrics=['mae', 'acc'])


	def train(self, no_big_epochs, no_fit_epochs, timestamps, batch_size=1000):
		# Training the model
		for i in range(0, no_big_epochs):
			print("\n\n\n  NEW EPOCH   NEW EPOCH   NEW EPOCH   NEW EPOCH   NEW EPOCH   NEW EPOCH   NEW EPOCH   NEW EPOCH ")
			print("\n\n")
			for timestep in timestamps:
				print("epoch ", i+1, "/", no_big_epochs, ", timestep ", timestep)
				self._data_builder.set_timestep(timestep)
				while 1:
					x, y, passed = self._data_builder.next_batch()
					self._model.fit(x, y, epochs=no_fit_epochs, batch_size=batch_size)
					if passed:
						break
				self.save_model()

	def save_model(self, path=None):
		model_json = self._model.to_json()
		if path:
			folder = path.rsplit("/", 1)[0]
			if not os.path.exists(folder):
				os.mkdir(folder)
		else:
			path = "models/" + self._model_name

		# SAVE MODEL
		if not os.path.exists("models"):
			os.mkdir("models")

		with open(path + ".json", "w") as json_file:
			json_file.write(model_json)
		# serialize weights to HDF5
		self._model.save_weights(path + ".h5")
		print("Saved model to disk")

	def load_model(self, path=None):
		# ######   LOAD MODEL
		# load json and create model
		if path:
			folder = path.rsplit("/", 1)[0]
			if not os.path.exists(folder):
				os.mkdir(folder)
		else:
			path = "models/" + self._model_name
		json_file = open(path + '.json', 'r')
		loaded_model_json = json_file.read()
		json_file.close()
		self._model = model_from_json(loaded_model_json)
		# load weights into new model
		self._model.load_weights(path + ".h5")
		print("Loaded model from disk")


	def predict(self, test_timesteps):
		# # ## TEST MODEL - Make predictions

		# predicted by model
		self._y_predicted_total = np.zeros((1, 13))
		# real data
		self._y_total = np.zeros((1, 13))


		for timestep in test_timesteps:
			print(timestep, "/", test_timesteps[-1])

			self._data_builder.set_timestep(timestep)

			while 1:
				x, y, passed = self._data_builder.next_batch(100000)
				y_predicted = self._model.predict(x)
				self._y_predicted_total = np.concatenate((self._y_predicted_total, y_predicted))
				self._y_total = np.concatenate((self._y_total, y))
				print("")
				if passed: break

		# Deleting initial zeroes
		self._y_total = self._y_total[1:]
		self._y_predicted_total = self._y_predicted_total[1:]


	### COMPUTE MEASURES
	def sum_squared_diffs(self, y: np.ndarray, y_pred: np.ndarray):
		rez = y - y_pred
		rez = np.square(rez)
		return sum(rez)

	def sum_of_abs(self, y: np.ndarray, y_pred: np.ndarray):
		rez = y - y_pred
		rez = np.abs(rez)
		return sum(rez)

	def count_nonzero(self, y:np.ndarray):
		count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		for l in y[:]:
			for k in range(l.shape[0]):
				if l[k] != 0:
					count[k] += 1
		return count


	def sum_of_abs_nonzero(self, y: np.ndarray, y_pred: np.ndarray, erori_mari):
		rez = y - y_pred
		rez = np.abs(rez)
		for l in range(13):

			for j in range(rez.shape[0]):
				e = rez[j, l]
				if e > 10 and y[j, l] != 0:
					erori_mari[l].append(e)
		return sum(rez)

	def compute_errors(self):
		# numar cate instante sunt (nu ca si cum e nevoie) si cate sunt non-zero
		num_of_instances = np.zeros((self._y_total.shape[1]))
		nb_of_nonzero_instances = np.zeros((self._y_total.shape[1]))
		for i in range(self._y_total.shape[0]):
			for j in range(self._y_total.shape[1]):
				num_of_instances[j] += 1
				if self._y_total[i, j] != 0:
					nb_of_nonzero_instances[j] += 1

		print("Total number of instances: ", num_of_instances)
		print("Total number of nonzero instances: ", nb_of_nonzero_instances)

		# MSE - Mean Squared Error - media dintre patratele diferentelor dintre prezis si real
		total_mse = self.sum_squared_diffs(self._y_total, self._y_predicted_total)/num_of_instances

		# MAE - Mean Absolute error - media dintre valoarea absoluta a diferentelor dintre prezis si real
		mae = self.sum_of_abs(self._y_total, self._y_predicted_total)/num_of_instances

		print("Mean squared Error: ", total_mse, " => ", np.average(total_mse))
		# RMSE - Root Mean Squared Error - radical din MSE
		print("RMSE: ", np.sqrt(total_mse), " => ", np.average(np.sqrt(total_mse)))
		print("MAE: ", mae, " => ", np.average(mae))

		# Standard deviation pe erori - media dintre patratele diferentelor dintre MAE si valoarea absoluta a diferentei
		# dintre prezis si real
		standard_deviation_sum = np.zeros((self._y_total.shape[1]))
		count = np.zeros((self._y_total.shape[1]))
		for i in range(self._y_total.shape[0]):
			for j in range(self._y_total.shape[1]):
				standard_deviation_sum[j] += np.square(mae[j] - np.abs(self._y_total[i, j] - self._y_predicted_total[i, j]))
				count[j] += 1
		standard_deviation = np.sqrt(standard_deviation_sum/count)
		print("Standard deviation: ", standard_deviation, " => ", np.average(standard_deviation))

		#### NONZERO
		# pe non zero sunt aceleasi chestii doar calculate putin diferit
		erori_mari = [[], [], [], [], [], [], [], [], [], [], [], [], []]
		squared_sum_nonzero = np.zeros((self._y_total.shape[1]))
		mae_sum_nonzero = np.zeros((self._y_total.shape[1]))
		for i in range(self._y_total.shape[0]):
			for j in range(self._y_total.shape[1]):
				if self._y_total[i, j] != 0:
					squared_sum_nonzero[j] += np.square(self._y_total[i,j] - self._y_predicted_total[i, j])
					mae_sum_nonzero[j] += np.abs(self._y_total[i, j] - self._y_predicted_total[i, j])
					if np.abs(self._y_total[i, j] - self._y_predicted_total[i, j]) > 10:
						erori_mari[j].append(np.abs(self._y_total[i, j] - self._y_predicted_total[i, j]))
		total_mse_nonzero = squared_sum_nonzero / nb_of_nonzero_instances
		mae_nonzero = mae_sum_nonzero/nb_of_nonzero_instances
		print("Mean squared Error Nonzero: ", total_mse_nonzero, " => ", np.average(total_mse_nonzero))
		print("RMSE Nonzero: ", np.sqrt(total_mse_nonzero), " => ", np.average(np.  sqrt(total_mse_nonzero)))
		print("MAE Nonzero: ", mae_nonzero, " => ", np.average(mae_nonzero))

		nr_erori_mari = np.array([len(x) for x in erori_mari])
		print("Numar erori mari: ", nr_erori_mari)
		print("Procent erori mari: ", (nr_erori_mari*100)/nb_of_nonzero_instances)

		standard_deviation_sum_nonzero = np.zeros((self._y_total.shape[1]))
		for i in range(self._y_total.shape[0]):
			for j in range(self._y_total.shape[1]):
				standard_deviation_sum_nonzero[j] += np.square(mae_nonzero[j] - np.abs(self._y_total[i, j] - self._y_predicted_total[i, j]))
		standard_deviation_nonzero = np.sqrt(standard_deviation_sum_nonzero / nb_of_nonzero_instances)
		print("Standard deviation Nonzero: ", standard_deviation_nonzero, " => ", np.average(standard_deviation_nonzero))

		print("scikit rmse: ", np.sqrt(mean_squared_error(self._y_total, self._y_predicted_total)))
		print("scikit mae: ", mean_absolute_error(self._y_total, self._y_predicted_total))

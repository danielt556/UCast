import numpy as np
from core.config import Rs13, Vs13, VIL13
import core.fileHandler as fh


class BigCubeDataBuilder:
	"""
	Incarca un cub 4D in memorie.

	Returneaza date de antrenare in modelul punct cu vecini, pentru maxim un timestep.
	Deoarece pentru fiecare punct datele de antrenare sunt 13^3, uneori datele de
	antrenare pentru un intreg timestep nu incap in memorie. De aceea aceasta clasa
	e facuta sa tina minte un timestep, si sa returneze datele de antrenare pentru
	acel timestap in batch-uri mai mici. Practic, functioneaza ca un fel de iterator
	peste datele de antrenare pentru un timestep, dar in loc sa returneze doar un
	element, returneaza un batch de elemente si merge mai departe (a trebuit sa fac
	asta ca sa pot face teste mai usor pe leptopul meu)
	"""

	def __init__(self, input, nb_of_neighbours=13, products_to_use=None):
		if type(input) is str:
			self._input_cube = fh.load_one(input)
		elif type(input) is np.ndarray:
			self._input_cube = input
		else:
			raise ValueError("Invalid input. Must be a path(string) or the cube itself (numpy.ndarray)")

		if products_to_use is not None:
			self._input_cube = self._input_cube[:, :, :, products_to_use]

		self._nb_of_neighbours = nb_of_neighbours
		# row si column index sunt indecsii curenti pentru timestep-ul de unde se extrag datele de antrenare
		self._row_index = 0
		self._column_index = 0
		self.reset_indices()

		# timestep-ul curent
		self.__time_step = 0

	def set_timestep(self, timestep):
		self.__time_step = timestep

	def advance_timestep(self):
		# nu face verificare sa vada daca a ajuns la sfarsit
		self.__time_step += 1

	def cube_shape(self):
		return self._input_cube.shape

	def number_of_neighbours(self):
		return self._nb_of_neighbours

	def reset_indices(self):
		#asta pentru ca ignoram punctele care nu au toti vecinii, deci mergem doar de la linia 6 incolo
		self._row_index = self._nb_of_neighbours // 2
		self._column_index = self._nb_of_neighbours // 2

	def set_indices(self, row, column):
		self._row_index = row
		self._column_index = column

	# @staticmethod
	# def _read_cube(path: str) -> np.ndarray:
	# 	cube = load_point(path)
	# 	return cube

	def next_batch(self, size=40000):
		"""
		Functia asta returneaza un grup de date de antrenare egal cu marimea data de
		size (un batch de date de antrenare) si seteaza indecsii pregatindu-i pentru
		un nou batch (ca un fel de next pentru iterator).
		Daca in timestep au ramas mai putine elemente decat zice size o sa returneze
		un batch mai mic si reseteaza indecsii la inceputul timestep-ului. NU trece
		la urmatorul timestep.
		Pentru un cub micsorat pe harta la ~400x400 (cum foloseam eu ca nu antrenam
		pe toate imaginea) un size de 40.000 ar da cam 3 batch-uri.
		"""
		(_, nb_rows, nb_columns, _) = self._input_cube.shape
		radius = self._nb_of_neighbours // 2
		if nb_columns <= self._column_index + size + radius:
			remaining_columns = size - (nb_columns - self._column_index) + radius
			rez_input = self._input_cube[self.__time_step,
										self._row_index - radius:self._row_index + radius + 1,
			            				self._column_index - radius:self._column_index + radius + 1]
			rez_input = rez_input.flatten()
			s = rez_input.shape
			rez_input = np.zeros((size, s[0]))
			rez_output = np.zeros((1, self._input_cube.shape[3]))
			current_point_input = 0
			while nb_columns <= self._column_index + size + radius:
				for i in range(self._column_index, nb_columns - radius):
					temp = self._input_cube[self.__time_step,
											self._row_index - radius:self._row_index + radius + 1,
											i - radius:i + radius + 1]
					temp = temp.flatten()
					rez_input[current_point_input] += temp
					current_point_input += 1
				rez_output2 = self._input_cube[self.__time_step + 1,
												self._row_index,
												self._column_index:nb_columns - radius]
				rez_output = np.concatenate((rez_output, rez_output2))
				self._row_index += 1
				self._column_index = radius
				size = remaining_columns
				remaining_columns = size - (nb_columns - self._column_index) + radius

				if self._row_index + radius >= nb_rows:
					print("batch incomplete, reached the end of the cube. Indices reseted.")
					self.reset_indices()
					rez_input = rez_input[:current_point_input]
					rez_output = rez_output[1:]
					return rez_input, rez_output, True

			for i in range(radius, size + radius):
				temp = self._input_cube[self.__time_step,
										self._row_index - radius:self._row_index + radius + 1,
										i - radius:i + radius + 1]
				temp = temp.flatten()
				rez_input[current_point_input] += temp
				current_point_input += 1
			rez_output2 = self._input_cube[self.__time_step + 1, self._row_index, radius:size + radius]
			rez_output = np.concatenate((rez_output, rez_output2))
			rez_output = rez_output[1:]
			self._column_index += size

			return rez_input, rez_output, False
		else:
			rez_input = self._input_cube[self.__time_step,
										self._row_index - radius:self._row_index + radius + 1,
										self._column_index - radius:self._column_index + radius + 1]
			rez_input = rez_input.flatten()
			s = rez_input.shape
			rez_input = rez_input.reshape((1, s[0]))
			for i in range(self._column_index + 1, self._column_index + size):
				temp = self._input_cube[self.__time_step, self._row_index - radius:self._row_index + radius + 1,
				       i - radius:i + radius + 1]
				temp = temp.flatten()
				s = temp.shape
				temp = temp.reshape((1, s[0]))
				rez_input = np.concatenate((rez_input, temp))
			rez_output = self._input_cube[self.__time_step + 1,
											self._row_index,
											self._column_index:self._column_index + size]
			self._column_index += size

			return rez_input, rez_output, False

	def crop_cube(self, nb_of_columns_to_drop: int):
		"""
		Pastreaza doar centrul cubului astfel incat sa fie sterse
		nb_of_columns_to_drop coloane si sa pastreze proportia, (adica stergant un
		numar de linii astfel incat imaginea sa aiba aceleasi proportii).
		De exemplu, daca imaginea de intraree e 800x624, si se apeleaza
		crop_cube(400), imaginea rezultata va fii 400x312, mai exact matricea 400x312
		din centrul imaginii originale.
		"""
		print("initial shape = ", self._input_cube.shape)
		(_, nb_of_rows, nb_of_columns, _) = self._input_cube.shape
		difference = nb_of_columns - nb_of_columns_to_drop
		proportion = difference / nb_of_columns
		row_difference = int(nb_of_rows * proportion)
		nb_of_rows_to_drop = nb_of_rows - row_difference

		first_column = nb_of_columns_to_drop // 2
		print("first column = ", first_column)
		first_line = nb_of_rows_to_drop // 2
		print("first line = ", first_line)

		last_column = first_column + difference
		print("last column = ", last_column)
		last_line = first_line + row_difference
		print("last line = ", last_line)

		self.crop_cube_by_exact(first_line, last_line, first_column, last_column)
		print("resultet shape = ", self._input_cube.shape)
		print("output shape = ", self._input_cube.shape)

	def crop_cube_by_exact(self, first_line, last_line, first_column, last_column):
		self._input_cube = self._input_cube[:, first_line:last_line, first_column:last_column]
		self.reset_indices()

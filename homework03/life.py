import pathlib
import random
import copy

from typing import List, Optional, Tuple


Cell = Tuple[int, int]
Cells = List[int]
Grid = List[Cells]


class GameOfLife:

    def __init__(
        self,
        size: Tuple[int, int],
        randomize: bool=True,
        max_generations: Optional[float]=float('inf')
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool=False) -> Grid:
        """
        Создание списка клеток.

        Клетка считается живой, если ее значение равно 1, в противном случае клетка
        считается мертвой, то есть, ее значение равно 0.

        Parameters
        ----------
        randomize : bool
            Если значение истина, то создается матрица, где каждая клетка может
            быть равновероятно живой или мертвой, иначе все клетки создаются мертвыми.

        Returns
        ----------
        out : Grid
            Матрица клеток размером `cell_height` х `cell_width`.
        """
        if randomize == True:
            self.curr_generation = []
            for i in range(self.rows):
                underlist_cell = []
                for j in range(self.cols):
                    underlist_cell += [random.randint(0,1)]
                self.curr_generation += [underlist_cell]

            pass
        else:
            self.curr_generation = []
            for i in range(self.rows):
                underlist_cell = []
                for j in range(self.cols):
                    underlist_cell += [0]
                self.curr_generation += [underlist_cell]
        return self.curr_generation


    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Вернуть список соседних клеток для клетки `cell`.

        Соседними считаются клетки по горизонтали, вертикали и диагоналям,
        то есть, во всех направлениях.

        Parameters
        ----------
        cell : Cell
            Клетка, для которой необходимо получить список соседей. Клетка
            представлена кортежем, содержащим ее координаты на игровом поле.

        Returns
        ----------
        out : Cells
            Список соседних клеток.
        """
        list_neighbours = []
        cell_row, cell_col = cell
        for i in range(3):
            for j in range(3):
                nbcell_row = cell_row - 1 + i
                nbcell_col = cell_col - 1 + j
                if((nbcell_row, nbcell_col) != cell and nbcell_col >= 0 and nbcell_row >= 0 and nbcell_col < self.cols and nbcell_row < self.rows):
                    list_neighbours += [self.curr_generation[nbcell_row][nbcell_col]]
        return list_neighbours


    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.

        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """
        help_list = []
        for i in range(self.rows):
            underlist_cell = []
            for j in range(self.cols):
                underlist_cell += [0]
            help_list += [underlist_cell]
        for i in range(self.rows):
            for j in range(self.cols):
                count_neighbours = 0
                for nb_cell in self.get_neighbours((i,j)):
                    if nb_cell == 1:
                        count_neighbours += 1
                if self.curr_generation[i][j] == 1:
                    if count_neighbours == 2 or count_neighbours == 3:
                        help_list[i][j] = 1
                else:
                    if count_neighbours == 3:
                        help_list[i][j] = 1
        return help_list


    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = copy.deepcopy(self.curr_generation)
        self.curr_generation = self.get_next_generation()
        self.generations += 1


    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        if self.generations >= self.max_generations:
            return True
        else:
            return False

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return self.prev_generation != self.curr_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> 'GameOfLife':
        """
        Прочитать состояние клеток из указанного файла.
        """
        grid_file = open(filename)

        grid = grid_file.readlines()
        for i in range(len(grid)):
            grid[i] = list(map(int, list(grid[i][0:len(grid[i])-1])))
        life = GameOfLife((len(grid), len(grid[i])))
        life.curr_generation = grid

        grid_file.close()

        return life


    def save(filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        file = open(filename, 'w')
        for row in range(len(self.curr_generation)):
            file.write("".join(map(str, self.curr_generation[row])) + '\n')

        file.close()

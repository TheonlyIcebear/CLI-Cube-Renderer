import shutil, math, numpy as np, time, os

class Vector:
    def __init__(self, x=None, y=None, z=None, array=None):
        if array is None:
            self.x = x
            self.y = y
            self.z = z

        else:
            self.x, self.y, self.z = array

    @property
    def array(self):
        return np.array([self.x, self.y, self.z])

    def __str__(self):
        return str(self.array)

    def __matmul__(self, other):
        if isinstance(other, Vector):
            return np.matmul(self.array, other.array)

        elif isinstance(other, (np.ndarray, list)):
            return np.matmul(self.array, np.array(other))

        else:
            raise TypeError("Unsupported operand type for matrix multiplication")

    def __sub__(self, other):
        if isinstance(other, Vector):
            return Vector(array=self.array - other.array)

        elif isinstance(other, (np.ndarray, list)):
            return Vector(array=self.array - np.array(other))

        elif isinstance(other, (int, float, np.number)):
            return Vector(array=self.array - other)

        else:
            raise TypeError("Unsupported operand type for subtraction")

    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector(array=self.array + other.array)

        elif isinstance(other, (np.ndarray, list)):
            return Vector(array=self.array + np.array(other))

        elif isinstance(other, (int, float, np.number)):
            return Vector(array=self.array + other)

        else:
            raise TypeError("Unsupported operand type for subtraction")

    def __mul__(self, other):
        if isinstance(other, Vector):
            return Vector(array=self.array * other.array)

        elif isinstance(other, (np.ndarray, list)):
            return Vector(array=self.array * np.array(other))

        elif isinstance(other, (int, float, np.number)):
            return Vector(array=self.array * other)

        else:
            raise TypeError("Unsupported operand type for multiplication")

    def __truediv__(self, other):
        if isinstance(other, Vector):
            return Vector(array=self.array / other.array)

        elif isinstance(other, (np.ndarray, list)):
            return Vector(array=self.array / np.array(other))

        elif isinstance(other, (int, float, np.number)):
            return Vector(array=self.array / other)

        else:
            raise TypeError("Unsupported operand type for division")

    def _define_rotation_matrix(self, angles):
        x_angle, y_angle, z_angle = angles

        r_x = np.array([
            [np.cos(x_angle) , 0, np.sin(x_angle) ],
            [0               , 1,                0],
            [-np.sin(x_angle), 0,  np.cos(x_angle)]
        ])


        r_y = np.array([
            [1, 0              ,                0],
            [0, np.cos(y_angle), -np.sin(y_angle)],
            [0, np.sin(y_angle), np.cos(y_angle) ]
        ])


        r_z = np.array([
            [np.cos(z_angle), -np.sin(z_angle), 0],
            [np.sin(z_angle), np.cos(z_angle) , 0],
            [0              , 0               , 1]
        ])

        return r_x, r_y, r_z

    def rotate(self, x_angle, y_angle, z_angle):
        matrices = self._define_rotation_matrix((x_angle, y_angle, z_angle))

        coords = np.array([self.x, self.y, self.z])
        
        for matrix in matrices:
            coords = np.matmul(coords, matrix)
        
        self.x, self.y, self.z = coords


class Projector:
    def __init__(self):
        terminal_size = shutil.get_terminal_size()

        self.columns = 180
        self.rows = 60
        self.y_angle = 45
        self.d = -1

        
        # print('\n'.join(["0" * columns for _ in range(rows)]))
        self.clear()
    
    def clear(self):
        self.array = np.full((self.rows, self.columns), " ")

    def draw(self):
        os.system("cls")
        print('\n'.join([''.join(row) for row in self.array]), end="\n")

    def project(self, cylinders, vectors):
        result = []
        array = np.array(self.array)

        for cylinder, vector in zip(cylinders, vectors):
            angle, radius, height = cylinder
            x = np.sin(angle) * radius
            y = np.cos(angle) * radius * np.sin(self.y_angle) + height * np.cos(self.y_angle)

            x /= (1 + vector.z / self.d)
            y /= (1 + vector.z / self.d)


            x = (x + 1) / 2
            y = (y + 1) / 2

            clipped_x = np.clip(int(y * self.rows), 0, self.rows - 1)
            clipped_y = np.clip(int(x * self.columns), 0, self.columns-1)

            array[clipped_x, clipped_y] = "+"

        self.array = array
        

    def define_cylindrical(self, vector: Vector):
        angle = math.atan2(vector.x, vector.y)
        radius = math.sqrt( (vector.x ** 2) + (vector.y ** 2) )
        height = vector.z

        return (angle, radius, height)
        
    def interpolate(self, vector1: Vector, vector2: Vector, smoothness=50):
        delta = vector2 - vector1
        vectors = []

        for i in range(smoothness):
            vectors.append(vector1 + delta * (i/smoothness))

        return vectors

    def project_points(self, points):
        cylindrical_points = [self.define_cylindrical(vector) for vector in cube]

    def animation(self):
        x_angle = 0
        y_angle = 0
        cube = [
                Vector(-0.5, -0.5, -0.5),
                Vector(-0.5, -0.5, 0.5),
                Vector(-0.5, -0.5, -0.5),


                Vector(0.5, -0.5, -0.5),
                Vector(0.5, -0.5, 0.5),
                Vector(0.5, -0.5, -0.5),

                Vector(0.5, 0.5, -0.5),
                Vector(0.5, 0.5, 0.5),
                Vector(0.5, 0.5, -0.5),

                Vector(-0.5, 0.5, -0.5),
                Vector(-0.5, 0.5, 0.5),
                Vector(-0.5, 0.5, -0.5),

                Vector(-0.5, -0.5, -0.5),

                Vector(-0.5, -0.5, 0.5),
                Vector(0.5, -0.5, 0.5),
                Vector(0.5, 0.5, 0.5),
                Vector(-0.5, 0.5, 0.5),
                Vector(-0.5, -0.5, 0.5),


                Vector(-0.5, -0.5, -0.5)

            ]

        cube = [vector * 0.7 for vector in cube]
        count = 0

        old_time = time.perf_counter()

        while True:
            
            for vector in cube:
                vector.rotate(x_angle, y_angle, 0)

            speed = 1/(time.perf_counter() - old_time)

            print(speed)

            points = [self.define_cylindrical(vector) for vector in cube]

            interpolated_vectors = [self.interpolate(cube[i], cube[i + 1]) for i in range(len(cube) - 1)]

            interpolated_vectors = sum(interpolated_vectors, [])

            interpolated_points = [self.define_cylindrical(vector) for vector in interpolated_vectors]

            projector.project(points + interpolated_points, cube + interpolated_vectors)

            x_angle += np.pi/(90000) * speed
            y_angle += np.pi/(90000) * speed

            count += 1

            # projector.project([(i, 0.5, -0.5) for i in range(360)] + [(i, 0.5, 0.5) for i in range(360)])

            self.draw()
            self.clear()

            


if __name__ == "__main__":
    vector = Vector(1, 1, 1)
    vector.rotate(1, 1, 1)
    print(vector)

    projector = Projector()
    projector.animation()
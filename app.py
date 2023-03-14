import random
import math
from decimal import Decimal
#Thư viện để tạo bảng
from tabulate import tabulate
class Map:
    def __init__(self, cities, distances):
        self.cities = cities
        self.distances = distances

class SimulatedAnnealing:
    def __init__(self, map, initial_temperature, cooling_factor):
        self.map = map
        self.initial_temperature = initial_temperature
        self.cooling_factor = cooling_factor
    result = []
    # Tính toán khoảng cách giữa hai thành phố
    def distance(self, city1, city2):
        x1, y1 = self.map.cities[city1]
        x2, y2 = self.map.cities[city2]
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    # Tính toán chi phí của đường đi
    def cost(self, path):
        total_cost = 0
        for i in range(len(path) - 1):
            city1 = path[i]
            city2 = path[i + 1]
            total_cost += self.distance(city1, city2)
        return total_cost

    # Tạo một giải pháp ban đầu
    def initial_solution(self):
        solution = list(range(len(self.map.cities)))
        random.shuffle(solution)
        print("Giải pháp ban đầu:", str(solution))
        return solution

    # Sinh một giải pháp mới
    def generate_new_solution(self, current_solution):
        # Lựa chọn hai vị trí ngẫu nhiên
        i = random.randint(0, len(current_solution) - 1)
        j = random.randint(0, len(current_solution) - 1)
        # Hoán đổi hai thành phố ở hai vị trí đó
        new_solution = current_solution[:]
        new_solution[i], new_solution[j] = new_solution[j], new_solution[i]
        return new_solution

    # Thuật toán Simulated Annealing
    def solve(self):
        # Khởi tạo giải pháp ban đầu
        current_solution = self.initial_solution()
        # Lưu trữ giải pháp tốt nhất
        best_solution = current_solution[:]
        # Khởi tạo nhiệt độ ban đầu
        temperature = self.initial_temperature
        # Lặp lại cho đến khi nhiệt độ giảm đến giá trị nhỏ
        i = 0
        while temperature > 1e-5:
            i += 1
            # Lưu trữ giải pháp hiện tại
            temp_str = round(Decimal(temperature), 8)
            result = [i, temp_str, current_solution, self.cost(current_solution)]
            self.result.append(result)
            # Sinh một giải pháp mới
            new_solution = self.generate_new_solution(current_solution)
            # Tính toán sự khác biệt về chi phí giữa hai giải pháp
            delta = self.cost(new_solution) - self.cost(current_solution)
            # Nếu giải pháp mới tốt hơn giải pháp hiện tại, chấp nhận giải pháp mới
            if delta < 0:
                current_solution = new_solution[:]
                # Kiểm tra xem giải pháp mới có tốt hơn giải pháp tốt nhất hiện tại hay không
                if self.cost(current_solution) < self.cost(best_solution):
                    best_solution = current_solution[:]
                # Nếu giải pháp mới không tốt hơn giải pháp hiện tại
                else:
                # Tính xác suất chấp nhận giải pháp mới dựa trên nhiệt độ hiện tại
                    p = math.exp(-delta / temperature)
                    # Nếu xác suất chấp nhận giải pháp mới lớn hơn một giá trị ngẫu nhiên, chấp nhận giải pháp mới
                    if random.random() < p:
                        current_solution = new_solution[:]
                
            # Giảm nhiệt độ
            temperature = temperature*self.cooling_factor
            temp_str = round(Decimal(temperature), 8)
            # Trả về giải pháp tốt nhất
            
        return best_solution

def main():
    # Định nghĩa bản đồ
    cities = [
        (0, 0),
        (1, 2),
        (3, 1),
        (5, 3),
        (6, 5),
        (4, 6),
        (2, 5),
        (1, 4)
    ]
    distances = [
        [0, 2, 4, 6, 8, 10, 12, 14],
        [2, 0, 2, 4, 6, 8, 10, 12],
        [4, 2, 0, 2, 4, 6, 8, 10],
        [6, 4, 2, 0, 2, 4, 6, 8],
        [8, 6, 4, 2, 0, 2, 4, 6],
        [10, 8, 6, 4, 2, 0, 2, 4],
        [12, 10, 8, 6, 4, 2, 0, 2],
        [14, 12, 10, 8, 6, 4, 2, 0]
    ]
    map = Map(cities, distances)
    # Khởi tạo thuật toán
    initial_temperature = 100
    cooling_factor = 0.95
    sa = SimulatedAnnealing(map, initial_temperature, cooling_factor)
    # Giải bài toán
    best_solution = sa.solve()
    print("Giải pháp tốt nhất:", best_solution)
    print("Chi phí tốt nhất:", sa.cost(best_solution))
    # Hiển thị kết quả
    data = sa.result
    table = tabulate(data, headers=['Vòng lặp', 'Nhiệt độ', 'Giải pháp', 'Chi phí'], tablefmt='grid', floatfmt=".10f")
    print(table)
if __name__ == "__main__":
    main()
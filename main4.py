import numpy as np
# Словарь с названиями предметов и их идентификаторами
subjects = {
    0: "Математика",
    1: "Линейная алгебра",
    2: "Математический анализ",
    3: "Комплексный анализ",
    4: "Дифференциальные уравнения",
    5: "Математическая логика",
    6: "Физика",
    7: "Статистика",
    8: "Теоретическая механика",
    9: "Теория вероятности"
}
# Функция реализующая алгоритм Ли для поиска кратчайшего пути в графе
def lee_algorithm(adj_matrix, start_node, end_node, required_points):
    n = len(adj_matrix)
    queue = [(start_node, 0)]  # Добавляем в очередь пару (вершина, текущий вес)
    visited = [False] * n
    path = [] # Путь от начальной вершины до текущей
    total_weight = 0 # Общий вес пути
    total_points = 0 # Общее количество баллов

    while queue:
        node, weight = queue.pop(0)
        visited[node] = True
        path.append(subjects[node]) # Добавляем название текущей вершины в путь
        total_weight += weight

        if node == end_node:
            if total_points < required_points:
                print("Достигнута конечная вершина, но набрано недостаточно баллов.")
            else:
                print("Оптимальный путь по алгоритму Ли:", ' -> '.join(path))
                print("Кол-во балов:", total_points)
            return

        neighbors = np.nonzero(adj_matrix[node])[0]
        for neighbor in neighbors:
            if not visited[neighbor]:
                queue.append((neighbor, adj_matrix[node][neighbor])) # Добавляем соседние вершины в очередь
                if adj_matrix[node][neighbor] > 0:
                    total_points += adj_matrix[node][neighbor] # Накапливаем баллы посещаемых предметов

    print("Нет пути между вершинами", subjects[start_node], "и", subjects[end_node])

# Функция реализующая алгоритм Флойда-Уоршалла для поиска кратчайших путей в графе
def floyd_warshall_algorithm(adj_matrix):
    n = len(adj_matrix)
    dist_matrix = np.copy(adj_matrix)

    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist_matrix[i][j] > dist_matrix[i][k] + dist_matrix[k][j]:
                    dist_matrix[i][j] = dist_matrix[i][k] + dist_matrix[k][j]

    return dist_matrix
# Функция для вычисления оптимального пути для сдачи сессии
def calculate_optimal_path():
    subject_scores = {
        0: 20,
        1: 5,
        2: 10,
        3: 15,
        4: 30,
        5: 15,
        6: 30,
        7: 10,
        8: 20,
        9: 4.0
    }

    required_subjects = [0, 4, 6]  # Математика, Дифференциальные уравнения, Физика

    # Вычисление оптимального пути
    dist_matrix = floyd_warshall_algorithm(adj_matrix)
    total_score = 0
    optimal_path = []

    for dist_matrix in required_subjects:
        total_score += subject_scores[dist_matrix]
        optimal_path.append(dist_matrix)

    while total_score < 100:
        max_score = -1
        max_subject = ""

        for subject, score in subject_scores.items():
            if score > max_score and subject not in optimal_path and total_score + score >= 100:
                max_score = score
                max_subject = subject

        if max_subject:
            optimal_path.append(max_subject)
            total_score += max_score
        else:
            break

    if total_score >= 100:
        print("Оптимальный путь для сдачи сессии:", optimal_path)
    else:
        print("Невозможно набрать необходимое количество баллов.")


# Пример использования функции
adj_matrix = np.array([
    [0, 5, 10, 15, 30, 0, 30, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 15, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 10, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 20],
    [0, 0, 0, 0, 0, 0, 40, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
])

start_vertex = 0
target_vertex = 6
required_points = 100

lee_algorithm(adj_matrix, start_vertex, target_vertex, required_points)

calculate_optimal_path()

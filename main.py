import igraph as ig
import plotly.graph_objs as go
import plotly.offline as offline
import random

# Создаем дерево с использованием igraph
nr_vertices = 25
G = ig.Graph.Tree(nr_vertices, 2)  # Создаем сбалансированное дерево

# Генерируем случайные значения узлов
values = [random.randint(1, 100) for _ in range(nr_vertices)]
G.vs["value"] = values

# Нисходящий обход
def find_max_down(node):
    stack = [node]
    visited = set()  # Добавляем множество для отслеживания посещенных узлов
    max_value = float("-inf")
    while stack:
        current_node = stack.pop()
        if current_node.index in visited:  # Проверяем, был ли узел уже посещен
            continue
        visited.add(current_node.index)  # Добавляем узел в множество посещенных
        max_value = max(max_value, current_node["value"])
        # Добавляем соседей узла в стек, если они еще не были посещены
        for neighbor in current_node.neighbors(mode=ig.ALL):
            if neighbor.index not in visited:
                stack.append(neighbor)
    return max_value

max_value_down = find_max_down(G.vs[0])

# Восходящий обход
def find_max_up(node):
    stack = [node]
    visited = set()
    max_value = float("-inf")
    while stack:
        current_node = stack[-1]
        visited.add(current_node.index)
        unvisited_children = [child for child in current_node.neighbors(mode=ig.ALL) if child.index not in visited]
        if unvisited_children:
            stack.extend(unvisited_children)
        else:
            max_value = max(max_value, current_node["value"])
            stack.pop()
    return max_value

max_value_up = find_max_up(G.vs[0])
max_value=max_value_up
# Визуализируем дерево с использованием Plotly
lay = G.layout('rt')
position = {k: lay[k] for k in range(nr_vertices)}
Xn = [position[k][0] for k in range(nr_vertices)]
Yn = [-position[k][1] for k in range(nr_vertices)]

edges = G.get_edgelist()
Xe = []
Ye = []
for edge in edges:
    Xe += [position[edge[0]][0], position[edge[1]][0], None]
    Ye += [-position[edge[0]][1], -position[edge[1]][1], None]

labels = G.vs["value"]

max_value_nodes = [v.index for v in G.vs if v["value"] == max_value]

# Обнуляем значения всех узлов с максимальным значением, кроме первого
for i in max_value_nodes[1:]:  # Пропускаем первый узел
    G.vs[i]["value"] = 0

# Обновляем список меток
labels = G.vs["value"]



node_trace = go.Scatter(
    x=Xn,
    y=Yn,
    mode='markers+text',
    marker=dict(
        symbol=0,  # Используем значение 0 для точки
        size=18,
        color=['rgb(255, 0, 0)' if value == max_value else 'rgb(0, 0, 255)' for value in G.vs["value"]],  # Красим в красный цвет узлы с максимальным значением
        line=dict(color='rgb(50,50,50)', width=1)
    ),
    text=labels,
    textposition="bottom center",
    hoverinfo="text"
)

edge_trace = go.Scatter(x=Xe,
                        y=Ye,
                        mode='lines',
                        line=dict(color='rgb(210,210,210)', width=1),
                        hoverinfo='none')

layout = go.Layout(title='Tree with Reingold-Tilford Layout',
                   titlefont_size=16,
                   showlegend=False,
                   hovermode='closest',
                   margin=dict(b=0, l=0, r=0, t=0),
                   xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                   yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))

fig = go.Figure(data=[edge_trace, node_trace], layout=layout)

# Выводим максимальное значение узла с использованием нисходящего и восходящего обходов
print(f"Максимальное значение узла (нисходящий обход): {max_value_down}")
print(f"Максимальное значение узла (восходящий обход): {max_value_up}")

# Сохраняем граф в файл HTML
offline.plot(fig, filename='tree-plot.html')

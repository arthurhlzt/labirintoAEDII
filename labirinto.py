from collections import deque
import heapq

# I = início, F = fim, # = parede, . = casa livre
labirinto = [
    "..#######.##..",
    "#.....#.....#.",
    "#####.#.###.#.",
    "......#.#.#.#.",
    "#.#####.#.#.#.",
    "#I..#...#..F#.",
    "###.#.###.###.",
    "..#.#...#.#...",
    "#.#.#.#.#.#.##",
    "#...#.#.#.#.#.",
    "#.#####...#.#.",
    "........#...#.",
    ".####.###.###.",
    "...#..###.....",
]

def achar(lab, simbolo):
    for i, linha in enumerate(lab):
        if simbolo in linha:
            return (i, linha.index(simbolo))


DIRECOES = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # cima, direita, baixo, esquerda


def livre(lab, i, j):
    dentro = 0 <= i < len(lab) and 0 <= j < len(lab[0])
    return dentro and lab[i][j] != '#'


def montar_grafo(lab):
    grafo = {}
    for i in range(len(lab)):
        for j in range(len(lab[0])):
            if not livre(lab, i, j):
                continue
            grafo[(i, j)] = []
            for di, dj in DIRECOES:
                if livre(lab, i + di, j + dj):
                    grafo[(i, j)].append((i + di, j + dj))
    return grafo


def desenhar(lab, caminho):
    grade = [list(linha) for linha in lab]
    for i, j in caminho:
        if grade[i][j] == '.':
            grade[i][j] = '*'
    for linha in grade:
        print(''.join(linha))


def reconstruir(anterior, saida):
    if saida not in anterior:
        return []
    caminho = []
    atual = saida
    while atual is not None:
        caminho.append(atual)
        atual = anterior[atual]
    return caminho[::-1]


def visitar(grafo, atual, saida, anterior):
    if atual == saida:
        return True
    for vizinho in grafo[atual]:
        if vizinho not in anterior:
            anterior[vizinho] = atual
            if visitar(grafo, vizinho, saida, anterior):
                return True
    return False


def dfs(grafo, inicio, saida):
    anterior = {inicio: None}
    visitar(grafo, inicio, saida, anterior)
    return reconstruir(anterior, saida), len(anterior)


def bfs(grafo, inicio, saida):
    fila = deque([inicio])
    anterior = {inicio: None}
    while fila:
        atual = fila.popleft()
        if atual == saida:
            break
        for vizinho in grafo[atual]:
            if vizinho not in anterior:
                anterior[vizinho] = atual
                fila.append(vizinho)
    return reconstruir(anterior, saida), len(anterior)


def h(v, saida):
    return abs(v[0] - saida[0]) + abs(v[1] - saida[1])


def gulosa(grafo, inicio, saida):
    fronteira = [(h(inicio, saida), inicio)]
    anterior = {inicio: None}
    while fronteira:
        _, atual = heapq.heappop(fronteira)
        if atual == saida:
            break
        for vizinho in grafo[atual]:
            if vizinho not in anterior:
                anterior[vizinho] = atual
                heapq.heappush(fronteira, (h(vizinho, saida), vizinho))
    return reconstruir(anterior, saida), len(anterior)


grafo = montar_grafo(labirinto)
inicio = achar(labirinto, 'I')
saida = achar(labirinto, 'F')


def mostrar(nome, caminho):
    print()
    print(f'  {nome}')
    print()
    desenhar(labirinto, caminho)
    print()
    print('-' * 30)


caminho_dfs, casas_dfs = dfs(grafo, inicio, saida)
mostrar('DFS', caminho_dfs)

caminho_bfs, casas_bfs = bfs(grafo, inicio, saida)
mostrar('BFS', caminho_bfs)

caminho_gulosa, casas_gulosa = gulosa(grafo, inicio, saida)
mostrar('Gulosa', caminho_gulosa)

print()
print('Algoritmo | Passos | Casas visitadas')
print(f'DFS       | {len(caminho_dfs) - 1:>6} | {casas_dfs:>15}')
print(f'BFS       | {len(caminho_bfs) - 1:>6} | {casas_bfs:>15}')
print(f'Gulosa    | {len(caminho_gulosa) - 1:>6} | {casas_gulosa:>15}')

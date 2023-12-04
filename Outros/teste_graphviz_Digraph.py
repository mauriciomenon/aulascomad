from graphviz import Digraph

dot = Digraph()
dot.attr(rankdir='TB')  # Define a direção do layout de cima para baixo (Top-Bottom)

# Define o estilo dos nós
dot.attr('node', shape='rectangle', height='0.5', width='1.5', style='rounded')

# Adiciona o nó da estação controladora
dot.node('A', 'Controlling Station')

# Adiciona os nós das estações controladas
for i in range(1, 4):
    dot.node(f'B{i}', 'Controlled Station')

# Agrupa os nós das estações controladas em um mesmo rank
with dot.subgraph() as s:
    s.attr(rank='same')
    for i in range(1, 4):
        s.node(f'B{i}')

# Adiciona arestas invisíveis para forçar o alinhamento vertical
dot.attr('edge', style='invis')
dot.edge('A', 'B1')
dot.edge('B1', 'B2')
dot.edge('B2', 'B3')

# Adiciona as arestas visíveis da estação controladora para as estações controladas
# Usando constraint='false' para evitar influência no layout do gráfico
dot.attr('edge', style='solid', dir='forward', arrowhead='normal')
for i in range(1, 4):
    dot.edge('A', f'B{i}', constraint='false')

# Renderiza o gráfico em formato PNG
dot.render('flowchart', format='png', cleanup=True)

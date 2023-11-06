library(DiagrammeR)
library(rsvg)

grViz("
digraph dot {
rankdir=TB;
node [shape=rectangle, style=filled, fillcolor=white, fontname=Helvetica];
edge [color=black, dir=none, constraint=false];

// Ponto invisível para auxiliar na criação da linha vertical única
pointA [shape=point, width=0, height=0, label=\"\"];
pointB [shape=point, width=0, height=0, label=\"\"];
pointC [shape=point, width=0, height=0, label=\"\"];
pointD [shape=point, width=0, height=0, label=\"\"];
pointE [shape=point, width=0, height=0, label=\"\"];

// Estações
Controlling_Station [label=\"Controlling\nStation\"];
Controlled_StationA [label=\"Controlled\nStation A\"];
Controlled_StationB [label=\"Controlled\nStation B\"];
Controlled_StationC [label=\"Controlled\nStation C\"];
Controlled_StationD [label=\"Controlled\nStation D\"];

// Configuração dos nós e conexões
Controlling_Station -> pointA;
pointA -> pointB -> pointC -> pointD -> pointE;
pointA -> Controlled_StationA;
pointB -> Controlled_StationB;
pointC -> Controlled_StationC;
pointD -> Controlled_StationD;
}")

# Convert the DiagrammeR graph to SVG
svg_code <- DiagrammeR::to_svg(gr)

# Save the SVG code to a file
writeLines(svg_code, "c:\\Users\\menon\\git\\aulascomad\\Outros\\meu_grafico_combinado.svg")
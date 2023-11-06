library(DiagrammeR)
library(DiagrammeRsvg)

gr <- grViz("
digraph structures {
    node [shape=rectangle, style=filled, fillcolor=gray95]
    rankdir=TB;

    // Define nodes
    Controlling [label=\"Controlling Station\"];
    A [label=\"Controlled Station A\"];
    B [label=\"Controlled Station B\"];
    C [label=\"Controlled Station C\"];
    D [label=\"Controlled Station D\"];
    edge [dir=none];

    // Define relationships
    Controlling -> A [weight=10];
    Controlling -> B [weight=9];
    Controlling -> C [weight=8];
    Controlling -> D [weight=7];
}
")
from base.objects import TeXCommand
from base.collections import TeXCollection

class LaTeXEnvironment(TeXCollection):
    def __init__(self, env, objs):
        TeXCollection.__init__(self, objs)
        self.start = TeXCommand("begin", env).compile()
        self.end = TeXCommand("end", env).compile()
        self.sep = "\n"

def simple_latex_document(body):
    return TeXCollection([
                           TeXCommand("documentclass", "article", opts=["12pt"]),
                           TeXCommand("usepackage", "geometry", opts=["margin=1in"]),
                           TeXCommand("pagestyle", "empty"),
                           LaTeXEnvironment("document", body)
                         ], sep="\n").compile()

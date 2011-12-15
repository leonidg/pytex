from base.objects import TeXCommand
from base.collections import TeXCollection

class LaTeXEnvironment(TeXCollection):
    def __init__(self, env, objs=[]):
        TeXCollection.__init__(self, objs)
        # We need to add the \n by hand here because the separator
        # isn't included for the start/end delimiters
        self.start = TeXCommand("begin", env).compile() + "\n"
        self.end = "\n" + TeXCommand("end", env).compile()
        self.sep = "\n"

class LaTeXTabular(LaTeXEnvironment):
    def __init__(self, env, colfmt, objs=[]):
        LaTeXEnvironment.__init__(self, env, objs)
        self.start = TeXCommand("begin", env, colfmt).compile() + "\n"

def simple_latex_document(body):
    return TeXCollection([
                           TeXCommand("documentclass", "article", opts=["12pt"]),
                           TeXCommand("usepackage", "geometry", opts=["margin=1in"]),
                           TeXCommand("pagestyle", "empty"),
                           LaTeXEnvironment("document", body)
                         ], sep="\n").compile()

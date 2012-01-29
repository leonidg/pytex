from base.objects import TeXObject, TeXCommand
from base.collections import TeXCollection, TeXRow, TeXSet

class LaTeXEnvironment(TeXCollection):
    def __init__(self, env, objs=None):
        TeXCollection.__init__(self, objs)
        # We need to add the \n by hand here because the separator
        # isn't included for the start/end delimiters
        self.start = TeXSet([TeXCommand("begin", env), "\n"])
        self.end = TeXSet(["\n", TeXCommand("end", env)])
        self.sep = TeXObject("\n")

class LaTeXTabular(LaTeXEnvironment):
    def __init__(self, env, colfmt, objs=None):
        LaTeXEnvironment.__init__(self, env, objs)
        self.start = TeXSet([TeXCommand("begin", env, colfmt), "\n"])
    def addObj(self, obj):
        if len(self.objs) > 0:
            self.objs[-1].end = TeXRow.end
        obj.end = TeXObject()
        LaTeXEnvironment.addObj(self, obj)

def simple_latex_document(body, packages=None, pagestyle="empty"):
    if packages is None:
        packages = []
    extra_packages = TeXCollection(sep="\n")
    for package in packages:
        if type(package) is str:
            extra_packages.addObj(TeXCommand("usepackage", package))
        else:
            extra_packages.addObj(TeXCommand("usepackage", package[0], package[1]))
    return TeXCollection([
                           TeXCommand("documentclass", "article", opts=["12pt"]),
                           TeXCommand("usepackage", "geometry", opts=["margin=1in"]),
                           extra_packages,
                           TeXCommand("pagestyle", pagestyle),
                           LaTeXEnvironment("document", body)
                         ], sep="\n").compile()

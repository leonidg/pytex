from objects import TeXObject

class TeXCollection(TeXObject):
    """
    A collection of one ore more TeXObjects. When compiled, may be
    enclosed in some starting and ending strings and may have some
    separator.
    """
    start = TeXObject("")
    end = TeXObject("")
    sep = TeXObject(" ")
    def __init__(self, objs=None, start=None, end=None, sep=None):
        if objs is None:
            objs = []
        elif type(objs) is not list:
            objs = [objs]
        self.objs = objs
        if start is not None:
            self.start = TeXObject(start)
        if end is not None:
            self.end = TeXObject(end)
        if sep is not None:
            self.sep = TeXObject(sep)
    def addObj(self, obj):
        self.objs.append(obj)
    def compile(self):
        start = self.start.compile()
        sep = self.sep.compile()
        objs = map(lambda o: TeXObject(o).compile(), self.objs)
        end = self.end.compile()
        return "".join([start, sep.join(objs), end])

class TeXSet(TeXCollection):
    """
    A collection with no separator. This is useful for e.g a bunch of
    commands following one another
    """
    sep = TeXObject()

class TeXGroup(TeXCollection):
    """
    A semantically grouped collection. Often used for scope
    (e.g. "{\bf foo bar baz} quux" will limit the effect of
    the "\bf" to "foo bar baz".
    """
    start = TeXObject("{", raw=True)
    end = TeXObject("}", raw=True)

class TeXInlineMath(TeXCollection):
    start = TeXObject("$", raw=True)
    end = TeXObject("$", raw=True)
    sep = TeXObject()

class TeXBlockMath(TeXCollection):
    start = TeXObject("$$", raw=True)
    end = TeXObject("$$", raw=True)
    sep = TeXObject()

class TeXRow(TeXCollection):
    """
    A "row" that requires any sort of alignment or newline markers
    """
    end = TeXObject("\\\\", raw=True)
    sep = TeXObject(" & ", raw=True)

from objects import TeXObject

class TeXCollection(TeXObject):
    """
    A collection of one ore more TeXObjects. When compiled, may be
    enclosed in some starting and ending strings and may have some
    separator.
    """
    start = ""
    end = ""
    sep = " "
    def __init__(self, objs=[], start=None, end=None, sep=None):
        # This is sort of a hacky way to make the collections syntax
        # less strict and friendlier to reuse for math, etc.
        if type(objs) is not list:
            objs = [objs]
        self.objs = objs
        if start is not None:
            self.start = start
        if end is not None:
            self.end = end
        if sep is not None:
            self.sep = sep
    def addObj(self, obj):
        self.objs.append(obj)
    def compile(self):
        return self.start + self.sep.join(map(lambda o: TeXObject(o).compile(),
                                              self.objs)) + self.end

class TeXSet(TeXCollection):
    """
    A collection with no separator. This is useful for e.g a bunch of
    commands following one another
    """
    sep = ""

class TeXGroup(TeXCollection):
    """
    A semantically grouped collection. Often used for scope
    (e.g. "{\bf foo bar baz} quux" will limit the effect of
    the "\bf" to "foo bar baz".
    """
    start = "{"
    end = "}"

class TeXInlineMath(TeXCollection):
    start = "$"
    end = "$"
    sep = ""

class TeXBlockMath(TeXCollection):
    start = "$$"
    end = "$$"
    sep = ""

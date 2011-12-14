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
    def __init__(self, objs):
        # This is sort of a hacky way to make the collections syntax
        # less strict and friendlier to reuse for math, etc.
        if type(objs) is not list:
            objs = [objs]
        self.objs = objs
    def compile(self):
        collection = self.sep.join(map(lambda o: TeXObject(o).compile(),
                                       self.objs))
        return self.start + collection + self.end

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

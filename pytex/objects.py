class TeXObject(object):
    """
    Any generic object that in one way or another could be compiled by
    TeX. Generally speaking, this is either a string, a command, or a
    collection of strings and/or commands.
    """
    compile = str

class TeXCommand(TeXObject):
    """
    A TeX command. A command can have some arguments and
    options: \cmd[opt1,opt2,opt3=val,...]{arg1}{arg2}...
    """
    def __init__(self, cmd, *args, **opts):
        self.cmd = cmd
        self.args = args
        self.opts = opts
    def compile(self):
        arg_str = "".join(map(lambda s: "{%s}" % (s.compile(),),
                              self.args))
        opt_str = ""
        if len(self.opts) > 0:
            opt_strs = []
            for opt in self.opts:
                if self.opts[opt] is None:
                    opt_strs.append(opt)
                else:
                    opt_strs.append("%s=%s" % (opt, self.opts[opt]))
            opt_str = "[%s]" % (",".join(opt_strs),)
        return "\\%s%s%s" % (self.cmd, opt_str, arg_str)

class TeXCollection(TeXObject):
    """
    A collection of one ore more TeXObjects.
    """
    def __init__(self, objs):
        self.objs = objs
    def compile(self):
        return " ".join(map(lambda o: o.compile(),
                            self.objs))

class TeXGroup(TeXCollection):
    """
    A semantically grouped collection. Often used for scope
    (e.g. "{\bf foo bar baz} quux" will limit the effect of
    the "\bf" to "foo bar baz".
    """
    def compile(self):
        return "{%s}" % (TeXCollection.compile(self),)

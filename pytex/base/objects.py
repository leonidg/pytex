class TeXObject(object):
    """
    Any generic object that in one way or another could be compiled by
    TeX. This class exists solely to provide the universal .compile()
    interface for other functions and classes.

    When compiling using TeXObject, the hierarchy "collapses", so that
        TeXObject(TeXObject(TeXObject(foo))).compile()
    is equivalent to
        TeXObject(foo).compile()
    """
    def __init__(self, obj):
        self.obj = obj
    def compile(self):
        from pytex.util import tex_escape_string
        to_compile = self.obj
        while type(to_compile) is TeXObject:
            to_compile = to_compile.obj
        if type(to_compile) is str:
            return tex_escape_string(to_compile)
        else:
            return to_compile.compile()

class TeXCommand(TeXObject):
    """
    A TeX command. A command can have some arguments and
    options: \cmd[opt1,opt2,opt3=val,...]{arg1}{arg2}...
    """
    def __init__(self, cmd, *args, **kwargs):
        self.cmd = cmd
        self.args = args
        self.opts = []
        if 'opts' in kwargs:
            self.opts = kwargs['opts']
    def compile(self):
        arg_str = "".join(map(lambda s: "{%s}" % (TeXObject(s).compile(),),
                              self.args))
        opt_str = ""
        if len(self.opts) > 0:
            opt_str = "[%s]" % (",".join(self.opts),)
        return "\\%s%s%s" % (self.cmd, opt_str, arg_str)

class TeXEmptyCommand(TeXCommand):
    """
    A shortcut for an "empty" command. A good example is \TeX{}.
    Easier than doing TeXCommand("TeX", TeXObject("")) each time.
    """
    def __init__(self, cmd):
        TeXCommand.__init__(self, cmd, TeXObject(""))

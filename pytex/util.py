from base.objects import TeXObject, TeXCommand
from base.collections import TeXSet, TeXGroup, TeXInlineMath

class TeXEmptyCommand(TeXCommand):
    """
    A shortcut for an "empty" command. A good example is \TeX{}.
    Easier than doing TeXCommand("TeX", TeXObject("")) each time.
    """
    def __init__(self, cmd):
        TeXCommand.__init__(self, cmd, TeXObject(""))

def ensure_math(obj):
    return TeXSet([
                    TeXCommand("ifmmode"),
                    TeXGroup(obj),
                    TeXCommand("else"),
                    TeXGroup(obj),
                    TeXCommand("fi")
                  ])

def tex_escape_string(s):
    special_chars = {
                      "#": TeXCommand("#"),
                      "$": TeXCommand("$"),
                      "%": TeXCommand("%"),
                      "&": TeXCommand("&"),
                      "_": TeXCommand("_"),
                      "{": TeXCommand("{"),
                      "}": TeXCommand("}"),
                      "~": TeXEmptyCommand("~"),
                      "^": TeXEmptyCommand("^"),
                      "\\": ensure_math(TeXCommand("backslash")),
                    }
    escaped = []
    for c in s:
        if c in special_chars:
            escaped.append(special_chars[c].compile())
        else:
            escaped.append(c)
    return "".join(escaped)

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

def unmath(x):
    return TeXCommand("mbox", x)

def binary_math_operator(x, y, operator, math=(True, True)):
    """
    A generic function that combines two arguments with a binaryn
    operator. The optional "math" argument is a tuple specifying
    whether either the first or second argument should be treated as
    mathematical input.
    """
    # We'll use the identity function if we want math input (since
    # we'll be in ensure_math()) and otherwise unmath().
    identity = lambda x: x
    math_wrapper = [identity if math[i] else unmath  for i in (0, 1)]
    return ensure_math(TeXSet([math_wrapper[0](TeXObject(x)),
                               TeXObject(operator, raw=True),
                               math_wrapper[1](TeXObject(y))]))

def superscript(x, y, math=(True, True)):
    return binary_math_operator(x, y, operator="^", math=math)

def subscript(x, y, math=(True, True)):
    return binary_math_operator(x, y, operator="_", math=math)

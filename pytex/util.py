from objects import TeXObject, TeXCommand, TeXEmptyCommand
from collections import TeXCollection, TeXInlineMath

def ensure_math(obj):
    return TeXCollection([
                           TeXCommand("ifmmode"),
                           TeXObject(obj),
                           TeXCommand("else"),
                           TeXInlineMath(obj),
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
    return "".join([special_chars.get(c, TeXObject(c)).compile() for c in s])

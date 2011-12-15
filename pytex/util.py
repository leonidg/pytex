from base.objects import TeXObject, TeXCommand, TeXEmptyCommand
from base.collections import TeXSet, TeXInlineMath

def ensure_math(obj):
    return TeXSet([
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
    escaped = []
    for c in s:
        if c in special_chars:
            escaped.append(special_chars[c].compile())
        else:
            escaped.append(c)
    return "".join(escaped)

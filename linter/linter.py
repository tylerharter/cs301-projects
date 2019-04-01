import ast 
from collections import defaultdict, namedtuple

class Linter(ast.NodeVisitor):
    def __init__(self, suppressed=None):
        self.warn = namedtuple('WARN', 'name msg')
        self.forbidden_names = {"set", "list", "dict"}
        self.warnings = defaultdict(list)
        self.suppressed = suppressed if suppressed else [] 

    def show_warnings(self):
        for warning, linenos in self.warnings.items(): 
            if warning.name in self.suppressed:
                continue
            if len(linenos) == 1: 
                print("LINE %s : %s" % (linenos[0], warning.msg))
            else:
                print("LINES %s : %s" % (", ".join(map(str, linenos)), warning.msg))

    def register_warning(self, warning_name, warning_msg, lineno): 
        w = self.warn(warning_name, warning_msg)
        self.warnings[w].append(lineno)

    def visit_Name(self, node): 
        if node.id.lower() != node.id: 
            self.register_warning("snake_case", "The convention in Python is to use lowercase names, with words separated by '_', you used '%s'." % node.id, node.lineno)

        if len(node.id) == 1: 
            self.register_warning("descriptive", "Please try to use more descriptive variable names. You used : '%s'." % node.id, node.lineno)
        
        if node.id.lower() in self.forbidden_names:
            self.register_warning("keyword_names", "Please avoid using '%s' for a variable name, as it is a Python keyword." % node.id, node.lineno)


if __name__ == "__main__": 
    filename = 'demo1.py' 
    code = None
    with open(filename, 'r') as f:
        code = f.read()
    tree = ast.parse(code) 
    l = Linter(suppressed=['snake_case'])
    l.visit(tree)
    l.show_warnings()

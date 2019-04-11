import ast 
from collections import defaultdict, namedtuple

class Linter(ast.NodeVisitor):
    def __init__(self, suppressed=None):
        self.warn = namedtuple('WARN', 'name msg')
        self.forbidden_names = {"set", "list", "dict"}
        self.warnings = defaultdict(list)
        self.suppressed = suppressed if suppressed else [] 
        self.func_names = []

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

    def visit_FunctionDef(self, node): 
        # repeated names
        if node.name in self.func_names: 
            self.register_warning("repeated_function", 
                    "The function %s has more than one definition. Avoid reusing function names" % node.name, 
                    node.lineno)
        else:
            self.func_names.append(node.name) 

        # def BADNAME() 
        if node.name.lower() != node.name: 
            self.register_warning("snake_case", 
                    "The convention in Python is to use lowercase names for function names, with words separated by '_', you used '%s'." % node.name, 
                    node.lineno)

    def visit_Assign(self, node): 
        for target in node.targets:
            if type(target) == ast.Name:
                # a = 10
                if len(target.id) == 1: 
                    self.register_warning("descriptive", 
                            "Please try to use more descriptive variable names. You used : '%s'." % target.id, 
                            target.lineno)
                
                # list = [..]
                if target.id.lower() in self.forbidden_names:
                    self.register_warning("keyword_names", 
                            "Please avoid using '%s' for a variable name, as it is a Python keyword." % target.id, 
                            target.lineno)

                # x = x
                if type(node.value) == ast.Name and node.value.id == target.id: 
                    self.register_warning("self_assign", 
                            "Self assignment : the statement %s = %s is superflous" % (node.value.id, target.id), 
                            target.lineno)

    def visit_Compare(self, node): 
        # a == True
        if len(node.comparators) == 1: 
            if type(node.comparators[0]) == ast.NameConstant and node.comparators[0].value: 
                self.register_warning("unnnecessary_true", 
                        "Instead of doing something like 'if %s == True:', you can simply do, 'if a:'" % node.left.id, 
                        node.lineno)

    def visit_For(self, node): 
        if type(node.body[-1]) == ast.Continue: 
            self.register_warning("bad_continue", 
                    "A continue as the last statement in a loop is unnecessary, as the loop proceeds to the next iteration anyway", 
                    node.body[-1].lineno)

    def visit_Return(self, node): 
        pass 

if __name__ == "__main__": 
    filename = 'demo1.py' 
    code = None
    with open(filename, 'r') as f:
        code = f.read()
    tree = ast.parse(code) 
    l = Linter()
    l.visit(tree)
    l.show_warnings()

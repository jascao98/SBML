# Jason Cao
# 111004692

import sys
from ply.lex import TOKEN


# AST Nodes

class Node():
    def __init__(self):
        self.parent = None

    def parentCount(self):
        count = 0
        current = self.parent
        while current is not None:
            count += 1
            current = current.parent
        return count


# function definitions
class Program(Node):
    def __init__(self, function, block):
        super().__init__()
        self.functions = function
        self.main_block = block

    def eval(self):
        all_functions = self.functions

        for function in all_functions:
            if function.eval() == "Semantic Error":
                return "Semantic Error"

        if self.main_block.eval() == "Semantic Error":
            return "Semantic Error"

    def typecheck(self):
        all_functions = self.functions

        for function in all_functions:
            if function.typecheck() == "Semantic Error":
                return "Semantic Error"

        if self.main_block.typecheck() == "Semantic Error":
            return "Semantic Error"


# function definitions
class Function(Node):
    def __init__(self, funct_name, param, blocks, ret_val):
        super().__init__()
        self.function_name = funct_name
        self.parameters = param
        self.block = blocks
        self.ret = ret_val

    def eval(self):
        add_function = {}
        add_function["parameter"] = self.parameters
        add_function["block"] = self.block
        add_function["return"] = self.ret
        methods[self.function_name] = add_function

    def typecheck(self):
        if self.block.typecheck() == "Semantic Error":
            return "Semantic Error"

        if self.function_name in methods:
            return "Semantic Error"

        # function definitions


class Function_Call(Node):
    def __init__(self, funct_name, param):
        super().__init__()
        self.function_name = funct_name
        self.parameters = param

    def eval(self):
        method = methods[self.function_name]

        # check same length
        if len(self.parameters) != len(method["parameter"]):
            return "Semantic Error"

        local_var = {}
        index = 0;
        for i in self.parameters:
            temp = method["parameter"][index].value
            local_var[temp] = i.eval()
            index = index + 1

        stack.append(local_var)

        if method["block"].eval() == "Semantic Error":
            return "Semantic Error"

        return_val = method["return"].eval()
        stack.pop()
        return return_val

    def typecheck(self):
        return Function_Call


# block statements
class While_Block(Node):
    def __init__(self, condition, block):
        super().__init__()
        self.left = condition
        self.right = block

    def eval(self):

        while self.left.eval() == True:
            self.right.eval()

    def typecheck(self):
        if self.left.typecheck() == "Semantic Error":
            return "Semantic Error"
        if self.right.typecheck() == "Semantic Error":
            return "Semantic Error"


class IfElse_Block(Node):
    def __init__(self, condition, ifBlock, elseBlock):
        super().__init__()
        self.left = condition
        self.middle = ifBlock
        self.right = elseBlock

    def eval(self):
        leftStatement = self.left.eval()

        if leftStatement == "Semantic Error":
            return "Semantic Error"

        if leftStatement == True:
            if self.middle.eval() == "Semantic Error":
                return "Semantic Error"
        else:
            if self.right.eval() == "Semantic Error":
                return "Semantic Error"

    def typecheck(self):
        if self.left.typecheck() == "Semantic Error":
            return "Semantic Error"

        if self.middle.typecheck() == "Semantic Error":
            return "Semantic Error"

        if self.right.typecheck() == "Semantic Error":
            return "Semantic Error"


class If_Block(Node):
    def __init__(self, condition, block):
        super().__init__()
        self.left = condition
        self.right = block

    def eval(self):
        leftStatement = self.left.eval()

        if leftStatement == "Semantic Error":
            return "Semantic Error"

        if leftStatement == True:
            if self.right.eval() == "Semantic Error":
                return "Semantic Error"

    def typecheck(self):
        if self.left.typecheck() == "Semantic Error":
            return "Semantic Error"
        if self.right.typecheck() == "Semantic Error":
            return "Semantic Error"


class Eval_Block(Node):
    def __init__(self, val):
        super().__init__()
        self.value = val

    def eval(self):
        if self.value == 0:
            return "Print"
        for statement in self.value:
            if statement.eval() == "Semantic Error":
                return "Semantic Error"

    def typecheck(self):
        if self.value == 0:
            return "null"
        for statement in self.value:
            if statement.typecheck() == "Semantic Error":
                return "Semantic Error"


# type definitions--------------------------------------------
class Integer(Node):
    def __init__(self, val):
        super().__init__()
        self.value = val

    def eval(self):
        return int(self.value)

    # convert to int and check if valid
    def typecheck(self):
        try:
            if isinstance(int(self.value), int):
                return int
        except ValueError:
            return "Semantic Error"


class RealNumber(Node):
    def __init__(self, val):
        super().__init__()
        self.value = val

    def eval(self):
        return float(self.value)

    def typecheck(self):
        try:
            if isinstance(float(self.value), float):
                return float
        except ValueError:
            return "Semantic Error"


class AstString(Node):
    def __init__(self, val):
        super().__init__()
        self.value = val[1:-1]

    def eval(self):
        return str(self.value)

    def typecheck(self):
        try:
            if isinstance(str(self.value), str):
                return str

        except ValueError:
            return "Semantic Error"


class AstList(Node):
    def __init__(self, val):
        super().__init__()
        self.value = val

    def eval(self):
        return self.value

    def typecheck(self):
        if self.value == 0:
            self.value = []
            return list

        try:
            index = 0
            for i in self.value:
                self.value[index] = i.eval()
                if (type(self.value[index]) == list):
                    temp = 0
                    for j in self.value[index]:
                        self.value[index][temp] = j.eval()
                        temp += 1
                index += 1

            if isinstance(self.value, list):
                return list

        except TypeError:
            return "Semantic Error"


class AstTuple(Node):
    def __init__(self, val, comma):
        super().__init__()
        self.value = val
        self.hasComma = comma

    def eval(self):
        tupVal = '('
        for i in self.value:
            if type(i) == str:
                tupVal += '\''
                tupVal += i
                tupVal += '\''
            else:
                tupVal += str(i)
            tupVal += ', '
        tupVal = tupVal[0:-2]
        tupVal += ')'
        return tupVal

    def typecheck(self):
        try:
            index = 0
            for i in self.value:
                self.value[index] = i.eval()
                index += 1

            if isinstance(self.value, list):
                return AstTuple

        except TypeError:
            return "Semantic Error"


class AstTrue(Node):
    def __init__(self):
        super().__init__()
        self.value = True

    def eval(self):
        return self.value

    def typecheck(self):
        return AstTrue


class AstFalse(Node):
    def __init__(self):
        super().__init__()
        self.value = False

    def eval(self):
        return self.value

    def typecheck(self):
        return AstFalse


# operators=====================================
class Print(Node):
    def __init__(self, val):
        super().__init__()
        self.value = val

    def eval(self):
        print(self.value.eval())
        return "Print"

    def typecheck(self):
        if self.value.typecheck() == "Semantic Error":
            return "Semantic Error"


class Variable(Node):
    def __init__(self, val):
        super().__init__()
        self.value = val

    def eval(self):
        if len(stack) > 0 and self.value in stack[-1]:
            dict = stack[-1]
            return dict[self.value]
        else:
            return "Semantic Error"

    def typecheck(self):
        if len(stack) > 0 and self.value in stack[-1]:
            dict = stack[-1]
            return dict[self.value]
        else:
            return Variable


class Variable_Assign(Node):
    def __init__(self, var, val):
        super().__init__()
        self.left = var
        self.right = val

    def eval(self):
        if len(stack) > 0:
            dict = stack[-1]
            dict[self.left.value] = self.right.eval()

        return Variable

    def typecheck(self):
        if self.right != None and self.right.typecheck() == "Semantic Error":
            return "Semantic Error"

        if self.left != None and self.left.typecheck() == "Semantic Error":
            return "Semantic Error"


class Variable_Update(Node):
    def __init__(self, var, index, val):
        super().__init__()
        self.left = var
        self.middle = index
        self.right = val

    def eval(self):  # length checking
        index = self.middle.eval()
        if type(self.left.eval()) == list:
            if len(self.left.eval()) <= index:
                return "Semantic Error"
        else:
            return "Semantic Error"

        self.left.eval()[self.middle.eval()] = self.right.eval()
        return Variable

    def typecheck(self):
        if self.left is not None:
            if self.left.typecheck() == "Semantic Error":
                return "Semantic Error"

        if self.middle is not None:
            midCheck = self.middle.typecheck()
            if midCheck != int and midCheck != Variable:
                return "Semantic Error"

        if self.right is not None:
            if self.right.typecheck() == "Semantic Error":
                return "Semantic Error"


class Plus(Node):
    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right
        self.left.parent = self
        self.right.parent = self

    def eval(self):
        val1 = self.left.eval()
        val2 = self.right.eval()
        if val1 == "Semantic Error" or val2 == "Semantic Error":
            return "Semantic Error"

        return val1 + val2

    def typecheck(self):
        # check child then check current nodes
        if self.left is not None:
            firstType = self.left.typecheck()

        if self.right is not None:
            secondType = self.right.typecheck()

        if firstType == Variable or secondType == Variable:
            return

        if not (((firstType == int or firstType == None) and (
                secondType == int or secondType == float or secondType == None))
                or ((firstType == float or firstType == None) and (
                        secondType == int or secondType == float or secondType == None))
                or ((firstType == list or firstType == None) and (secondType == list or secondType == None))
                or ((firstType == str or firstType == None) and (secondType == str or secondType == None))):
            return "Semantic Error"


class Minus(Node):
    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right
        self.left.parent = self
        self.right.parent = self

    def eval(self):
        val1 = self.left.eval()
        val2 = self.right.eval()
        if val1 == "Semantic Error" or val2 == "Semantic Error":
            return "Semantic Error"
        return val1 - val2

    def typecheck(self):
        # check child then check current nodes
        if self.left is not None:
            firstType = self.left.typecheck()

        if self.right is not None:
            secondType = self.right.typecheck()

        if firstType == Variable or secondType == Variable:
            return

        if not (((firstType == int or firstType == None) and (
                secondType == int or secondType == float or secondType == None))
                or ((firstType == float or firstType == None) and (
                        secondType == int or secondType == float or secondType == None))):
            return "Semantic Error"


class Times(Node):
    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right
        self.left.parent = self
        self.right.parent = self

    def eval(self):
        val1 = self.left.eval()
        val2 = self.right.eval()
        if val1 == "Semantic Error" or val2 == "Semantic Error":
            return "Semantic Error"
        return val1 * val2

        return self.left.eval() * self.right.eval()

    def typecheck(self):
        # check child then check current nodes
        if self.left is not None:
            firstType = self.left.typecheck()

        if self.right is not None:
            secondType = self.right.typecheck()

        if firstType == Variable or secondType == Variable:
            return

        if not (((firstType == int or firstType == None) and (
                secondType == int or secondType == float or secondType == None))
                or ((firstType == float or firstType == None) and (
                        secondType == int or secondType == float or secondType == None))):
            return "Semantic Error"


class NormalDivide(Node):
    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right
        self.left.parent = self
        self.right.parent = self

    def eval(self):
        val1 = self.left.eval()
        val2 = self.right.eval()
        if val1 == "Semantic Error" or val2 == "Semantic Error":
            return "Semantic Error"
        return float(val1 / val2)

    def typecheck(self):
        # check child then check current nodes
        if self.left is not None:
            firstType = self.left.typecheck()

        if self.right is not None:
            secondType = self.right.typecheck()

        if firstType == Variable or secondType == Variable:
            return

        if self.right.eval() == 0:
            return "Semantic Error"

        if not (((firstType == int or firstType == None) and (
                secondType == int or secondType == float or secondType == None))
                or ((firstType == float or firstType == None) and (
                        secondType == int or secondType == float or secondType == None))):
            return "Semantic Error"


class IntegerDivide(Node):
    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right
        self.left.parent = self
        self.right.parent = self

    def eval(self):
        val1 = self.left.eval()
        val2 = self.right.eval()
        if val1 == "Semantic Error" or val2 == "Semantic Error":
            return "Semantic Error"
        return int(val1 / val2)

    def typecheck(self):
        # check child then check current nodes
        if self.left is not None:
            firstType = self.left.typecheck()

        if self.right is not None:
            secondType = self.right.typecheck()

        if firstType == Variable or secondType == Variable:
            return

        if self.right.eval() == 0:
            return "Semantic Error"

        if not ((firstType == int or firstType == None) and (secondType == int or secondType == None)):
            return "Semantic Error"


class Modulus(Node):
    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right
        self.left.parent = self
        self.right.parent = self

    def eval(self):
        val1 = self.left.eval()
        val2 = self.right.eval()
        if val1 == "Semantic Error" or val2 == "Semantic Error":
            return "Semantic Error"
        return val1 % val2

    def typecheck(self):
        # check child then check current nodes
        if self.left is not None:
            firstType = self.left.typecheck()

        if self.right is not None:
            secondType = self.right.typecheck()

        if firstType == Variable or secondType == Variable:
            return

        if not ((firstType == int or firstType == None) and (secondType == int or secondType == None)):
            return "Semantic Error"


class Exponent(Node):
    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right
        self.left.parent = self
        self.right.parent = self

    def eval(self):
        val1 = self.left.eval()
        val2 = self.right.eval()
        if val1 == "Semantic Error" or val2 == "Semantic Error":
            return "Semantic Error"
        return val1 ** val2

    def typecheck(self):
        # check child then check current nodes
        if self.left is not None:
            firstType = self.left.typecheck()

        if self.right is not None:
            secondType = self.right.typecheck()

        if firstType == Variable or secondType == Variable:
            return

        if not ((firstType == int or firstType == None) and (secondType == int or secondType == None)):
            return "Semantic Error"


# taken from in class ppt
class Negation(Node):
    def __init__(self, child):
        super().__init__()
        self.child = child
        self.child.parent = self

    def eval(self):
        val1 = self.child.eval()
        if val1 == "Semantic Error":
            return "Semantic Error"
        return not val1

    def typecheck(self):
        # check child then check current nodes
        if self.child is not None:
            checkType = self.child.typecheck()

        if checkType == Variable:
            return

        if not ((checkType == AstFalse) or (checkType == AstTrue)):
            return "Semantic Error"


class Conjunction(Node):
    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right
        self.left.parent = self
        self.right.parent = self

    def eval(self):
        val1 = self.left.eval()
        val2 = self.right.eval()
        if val1 == "Semantic Error" or val2 == "Semantic Error":
            return "Semantic Error"
        return val1 and val2

    def typecheck(self):
        # check child then check current nodes
        if self.left is not None:
            firstType = self.left.typecheck()

        if self.right is not None:
            secondType = self.right.typecheck()

        if firstType == Variable or secondType == Variable:
            return

        if not ((firstType == AstTrue or firstType == AstFalse or firstType == None) and (
                secondType == AstTrue or secondType == AstFalse or secondType == None)):
            return "Semantic Error"


class Disjunction(Node):
    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right
        self.left.parent = self
        self.right.parent = self

    def eval(self):
        val1 = self.left.eval()
        val2 = self.right.eval()
        if val1 == "Semantic Error" or val2 == "Semantic Error":
            return "Semantic Error"
        return val1 or val2

    def typecheck(self):
        # check child then check current nodes
        if self.left is not None:
            firstType = self.left.typecheck()

        if self.right is not None:
            secondType = self.right.typecheck()

        if firstType == Variable or secondType == Variable:
            return

        if not ((firstType == AstTrue or firstType == AstFalse or firstType == None) and (
                secondType == AstTrue or secondType == AstFalse or secondType == None)):
            return "Semantic Error"


class LessThan(Node):
    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right
        self.left.parent = self
        self.right.parent = self

    def eval(self):
        val1 = self.left.eval()
        val2 = self.right.eval()
        if val1 == "Semantic Error" or val2 == "Semantic Error":
            return "Semantic Error"
        return val1 < val2

    def typecheck(self):
        # check child then check current nodes
        if self.left is not None:
            firstType = self.left.typecheck()

        if self.right is not None:
            secondType = self.right.typecheck()

        if firstType == Variable or secondType == Variable:
            return

        if not (((firstType == int or firstType == None) and (
                secondType == int or secondType == float or secondType == None))
                or ((firstType == float or firstType == None) and (
                        secondType == int or secondType == float or secondType == None))
                or ((firstType == str or firstType == None) and (secondType == str or secondType == None))):
            return "Semantic Error"


class LessEqual(Node):
    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right
        self.left.parent = self
        self.right.parent = self

    def eval(self):
        val1 = self.left.eval()
        val2 = self.right.eval()
        if val1 == "Semantic Error" or val2 == "Semantic Error":
            return "Semantic Error"
        return val1 <= val2

    def typecheck(self):
        # check child then check current nodes
        if self.left is not None:
            firstType = self.left.typecheck()

        if self.right is not None:
            secondType = self.right.typecheck()

        if firstType == Variable or secondType == Variable:
            return

        if not (((firstType == int or firstType == None) and (
                secondType == int or secondType == float or secondType == None))
                or ((firstType == float or firstType == None) and (
                        secondType == int or secondType == float or secondType == None))
                or ((firstType == str or firstType == None) and (secondType == str or secondType == None))):
            return "Semantic Error"


class NotEqual(Node):
    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right
        self.left.parent = self
        self.right.parent = self

    def eval(self):
        val1 = self.left.eval()
        val2 = self.right.eval()
        if val1 == "Semantic Error" or val2 == "Semantic Error":
            return "Semantic Error"
        return val1 != val2

    def typecheck(self):
        # check child then check current nodes
        if self.left is not None:
            firstType = self.left.typecheck()

        if self.right is not None:
            secondType = self.right.typecheck()

        if firstType == Variable or secondType == Variable:
            return

        if not (((firstType == int or firstType == None) and (
                secondType == int or secondType == float or secondType == None))
                or ((firstType == float or firstType == None) and (
                        secondType == int or secondType == float or secondType == None))
                or ((firstType == str or firstType == None) and (secondType == str or secondType == None))):
            return "Semantic Error"


class EqualTo(Node):
    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right
        self.left.parent = self
        self.right.parent = self

    def eval(self):
        val1 = self.left.eval()
        val2 = self.right.eval()
        if val1 == "Semantic Error" or val2 == "Semantic Error":
            return "Semantic Error"
        return val1 == val2

    def typecheck(self):
        # check child then check current nodes
        if self.left is not None:
            firstType = self.left.typecheck()

        if self.right is not None:
            secondType = self.right.typecheck()

        if firstType == Variable or secondType == Variable:
            return

        if not (((firstType == int or firstType == None) and (
                secondType == int or secondType == float or secondType == None))
                or ((firstType == float or firstType == None) and (
                        secondType == int or secondType == float or secondType == None))
                or ((firstType == str or firstType == None) and (secondType == str or secondType == None))):
            return "Semantic Error"


class GreaterThan(Node):
    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right
        self.left.parent = self
        self.right.parent = self

    def eval(self):
        val1 = self.left.eval()
        val2 = self.right.eval()
        if val1 == "Semantic Error" or val2 == "Semantic Error":
            return "Semantic Error"
        return val1 > val2

    def typecheck(self):
        # check child then check current nodes
        if self.left is not None:
            firstType = self.left.typecheck()

        if self.right is not None:
            secondType = self.right.typecheck()

        if firstType == Variable or secondType == Variable:
            return

        if not (((firstType == int or firstType == None) and (
                secondType == int or secondType == float or secondType == None))
                or ((firstType == float or firstType == None) and (
                        secondType == int or secondType == float or secondType == None))
                or ((firstType == str or firstType == None) and (secondType == str or secondType == None))):
            return "Semantic Error"


class GreaterEqual(Node):
    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right
        self.left.parent = self
        self.right.parent = self

    def eval(self):
        val1 = self.left.eval()
        val2 = self.right.eval()
        if val1 == "Semantic Error" or val2 == "Semantic Error":
            return "Semantic Error"
        return val1 >= val2

    def typecheck(self):
        # check child then check current nodes
        if self.left is not None:
            firstType = self.left.typecheck()

        if self.right is not None:
            secondType = self.right.typecheck()

        if firstType == Variable or secondType == Variable:
            return

        if not (((firstType == int or firstType == None) and (
                secondType == int or secondType == float or secondType == None))
                or ((firstType == float or firstType == None) and (
                        secondType == int or secondType == float or secondType == None))
                or ((firstType == str or firstType == None) and (secondType == str or secondType == None))):
            return "Semantic Error"


class Indexing(Node):
    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right
        self.right.parent = self
        self.left.parent = self

    def eval(self):
        val1 = self.left.eval()
        val2 = self.right.eval()
        if val1 == "Semantic Error" or val2 == "Semantic Error":
            return "Semantic Error"
        return val1[val2]

    def typecheck(self):
        # check child then check current nodes
        if self.left is not None:
            firstType = self.left.typecheck()

        if self.right is not None:
            secondType = self.right.typecheck()

        if firstType == Variable or secondType == Variable:
            return

        if not (((firstType == str or firstType == "variable" or firstType == None or firstType == list) and (
                secondType == int or secondType == None))):
            return "Semantic Error"

        if len(self.left.eval()) <= self.right.eval():
            return "Semantic Error"


class Membership(Node):
    def __init__(self, left, right, valid):
        super().__init__()
        self.check = valid
        if type(right) == AstList or type(right) == AstString:
            self.left = left
            self.right = right
            self.left.parent = self
            self.right.parent = self
        else:
            self.check = False

    def eval(self):
        val1 = self.left.eval()
        val2 = self.right.eval()
        if val1 == "Semantic Error" or val2 == "Semantic Error":
            return "Semantic Error"
        return val1 in val2

    def typecheck(self):
        # check child then check current nodes
        if self.check == False:
            return "Semantic Error"

        if self.right is not None:
            secondType = self.right.typecheck()

        if secondType == Variable:
            return

        if not ((secondType == str or secondType == list or secondType == None)):
            return "Semantic Error"


class Cons(Node):
    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right
        self.left.parent = self
        self.right.parent = self

    def eval(self):
        val1 = self.left.eval()
        val2 = self.right.eval()
        if val1 == "Semantic Error" or val2 == "Semantic Error":
            return "Semantic Error"

        newList = self.right.eval().insert(0, self.left.eval())
        return self.right.eval()

    def typecheck(self):
        # check child then check current nodes
        if self.right is not None:
            secondType = self.right.typecheck()
        if self.left is not None:
            self.left.typecheck()

        if secondType == Variable:
            return

        if not (((secondType == list or secondType == None))):
            return "Semantic Error"


class TupleIndexing(Node):
    def __init__(self, num, atuple):
        super().__init__()
        self.left = num
        self.right = atuple

    def eval(self):
        if self.left.eval() == "Semantic Error":
            return "Semantic Error"
        return self.right[self.left.eval() - 1]

    def typecheck(self):
        if not self.left.typecheck() == int:
            return "Semantic Error"

        if self.left.eval() > len(self.right):
            return "Semantic Error"

        try:
            index = 0
            for i in self.right:
                self.right[index] = i.eval()
                index += 1

            if isinstance(self.right, list):
                return AstTuple

        except TypeError:
            return "Semantic Error"


# first name tokens
# numbers first
tokens = [
    'LEFT_PARENTHESIS',
    'RIGHT_PARENTHESIS',
    'INTEGER',
    'REAL',
    'PLUS',
    'MINUS',
    'TIMES',
    'NORMAL_DIVIDE',
    'EXPONENT',
    # booleans and strings, list and its operators
    'OPEN_INDEXING',
    'CLOSE_INDEXING',
    'TUPLE_INDEXING',
    'CONS',
    'LESS_THAN',
    'LESS_EQUAL',
    'EQUAL_TO',
    'NOT_EQUAL',
    'GREATER_EQUAL',
    'GREATER_THAN',
    'COMMA',
    'SEMICOLON',
    'EQUAL',
    'VARIABLE',
    'STRING',
    'OPEN_CURL',
    'CLOSE_CURL',
]

reserved = {
    'fun': 'FUNCTION',
    'True': 'TRUE',
    'False': 'FALSE',
    'in': 'MEMBERSHIP',
    'not': 'NEGATION',
    'andalso': 'CONJUNCTION',
    'orelse': 'DISJUNCTION',
    'div': 'INTEGER_DIVIDE',
    'mod': 'MODULUS',
    'print': 'PRINT',
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
}

tokens += reserved.values()

# specify tokens
t_FUNCTION = r"fun"
t_WHILE = r'while'
t_ELSE = r'else'
t_OPEN_CURL = r'{'
t_CLOSE_CURL = r'}'
t_IF = r'if'
t_PRINT = r'print'
t_EQUAL = r'='
t_SEMICOLON = r';'
t_LEFT_PARENTHESIS = r'\('
t_RIGHT_PARENTHESIS = r'\)'
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_NORMAL_DIVIDE = r'/'
t_INTEGER_DIVIDE = r'div'
t_MODULUS = r'mod'
t_EXPONENT = r'\*\*'
t_MEMBERSHIP = r'in'
t_CONS = r'::'
t_NEGATION = r'not'
t_CONJUNCTION = r'andalso'
t_DISJUNCTION = r'orelse'
t_LESS_THAN = r'<'
t_LESS_EQUAL = r'<='
t_NOT_EQUAL = r'<>'
t_EQUAL_TO = r'=='
t_GREATER_EQUAL = r'>='
t_GREATER_THAN = r'>'
t_OPEN_INDEXING = r'\['
t_CLOSE_INDEXING = r'\]'
t_TUPLE_INDEXING = r'\#'
t_TRUE = r"True"
t_FALSE = r"False"
t_COMMA = r','

# for strings
stringDouble = r'"[^\'"]*"'
stringSingle = r'\'[^\'"]*\''
inputString = stringDouble + r'|' + stringSingle


@TOKEN(inputString)
def t_STRING(t):
    return t


# for real numbers
normalReal = r'[\d]*\.[\d]*'
eReal = r'[\d]*\.[\d]*e-?[\d]+'
realNumber = normalReal + r'|' + eReal


@TOKEN(realNumber)
def t_REAL(t):
    return t


def t_INTEGER(t):
    r'-?\d+'
    return t


def t_VARIABLE(t):
    '[a-zA-Z][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'VARIABLE')  # Check for reserved words
    return t


# Ignored spaces and tabs
t_ignore = ' \t'


# count line number
# from demo files in class
def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


# print syntax and then go to next line
def t_error(t):
    t.lexer.skip(1)


# initialize lexer
import ply.lex as lex

# lexer = lex.lex(debug = True)
lexer = lex.lex()

# Parsing rule=====================
stack = []
global_var = {}
stack.append(global_var)
methods = {}

# Precedence
precedence = (
    ('left', 'DISJUNCTION'),
    ('left', 'CONJUNCTION'),
    ('left', 'NEGATION'),
    ('left', 'LESS_THAN', 'LESS_EQUAL', 'EQUAL_TO', 'NOT_EQUAL', 'GREATER_EQUAL', 'GREATER_THAN'),
    ('right', 'CONS'),
    ('left', 'MEMBERSHIP'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'NORMAL_DIVIDE', 'INTEGER_DIVIDE', 'MODULUS'),
    ('right', 'EXPONENT'),
    ('left', 'OPEN_INDEXING', 'CLOSE_INDEXING'),
    ('left', 'TUPLE_INDEXING'),
    # ('left','TUPLE'),
    ('left', 'LEFT_PARENTHESIS', 'RIGHT_PARENTHESIS', 'PAREN_GROUP'),
    ('right', 'UMINUS'),)


# Production rules
# variable======

def p_sbml_program(t):
    '''sbml_program : sbml_elements block
    | block'''
    if len(t) == 2:
        t[0] = Program(None, t[1])
    else:
        t[0] = Program(t[1], t[2])


def p_sbml_elements(t):
    '''sbml_elements : function
    | function sbml_elements'''
    if len(t) == 2:
        t[0] = [t[1]]
    else:
        t[2].insert(0, t[1])
        t[0] = t[2]
        t[0] = t[1]


def p_function_definition(t):
    'function : FUNCTION VARIABLE  LEFT_PARENTHESIS comma_elements RIGHT_PARENTHESIS EQUAL block expression SEMICOLON'
    t[0] = Function(t[2], t[4], t[7], t[8])


def p_block(t):
    '''block : OPEN_CURL CLOSE_CURL
    | OPEN_CURL multiple_statements CLOSE_CURL'''
    if len(t) == 4:
        t[0] = Eval_Block(t[2])
    else:
        t[0] = Eval_Block(0)


def p_while_statement(t):
    'statement : WHILE LEFT_PARENTHESIS expression RIGHT_PARENTHESIS block'
    t[0] = While_Block(t[3], t[5])


def p_if_else_statement(t):
    'statement : IF LEFT_PARENTHESIS expression RIGHT_PARENTHESIS block ELSE block'
    t[0] = IfElse_Block(t[3], t[5], t[7])


def p_if_statement(t):
    'statement : IF LEFT_PARENTHESIS expression RIGHT_PARENTHESIS block'
    t[0] = If_Block(t[3], t[5])


def p_multiple_statements(t):
    '''multiple_statements : statement
    |  statement multiple_statements'''
    if len(t) == 2:
        t[0] = [t[1]]
    else:
        t[2].insert(0, t[1])
        t[0] = t[2]


def p_statement(t):
    'statement : expression SEMICOLON'
    t[0] = t[1]


def p_function_call(t):
    '''expression : VARIABLE LEFT_PARENTHESIS comma_elements RIGHT_PARENTHESIS
    |  VARIABLE LEFT_PARENTHESIS RIGHT_PARENTHESIS'''
    if len(t) == 5:
        t[0] = Function_Call(t[1], t[3])
    else:
        t[0] = Function_Call(t[1], None)


def p_variable_assignment(t):
    'statement : var EQUAL expression SEMICOLON'
    t[0] = Variable_Assign(t[1], t[3])


def p_variable_update(t):
    'statement : expression OPEN_INDEXING expression CLOSE_INDEXING EQUAL expression SEMICOLON'
    t[0] = Variable_Update(t[1], t[3], t[6])


def p_variable(t):
    'var : VARIABLE'
    t[0] = Variable(t[1])


# doesnt work
def p_var(t):
    'expression : var'
    t[0] = t[1]


def p_print_statement(t):
    'statement : PRINT LEFT_PARENTHESIS expression RIGHT_PARENTHESIS SEMICOLON'
    t[0] = Print(t[3])


# parenthesis
def p_parenthesis_group(t):
    'expression : LEFT_PARENTHESIS expression RIGHT_PARENTHESIS %prec PAREN_GROUP'
    t[0] = t[2]


# negative sign
def p_expr_uminus(t):
    'expression : MINUS expression %prec UMINUS'
    t[0] = -t[2]


# rule for numbers~~
def p_integer(t):
    'expression : INTEGER'
    t[0] = Integer(t[1])


def p_real(t):
    'expression : REAL'
    t[0] = RealNumber(t[1])


# boolean propositions~~~~~~~~~~~~~~~

def p_expression_binop(t):
    '''expression : expression PLUS expression
    | expression MINUS expression
    | expression TIMES expression
    | expression NORMAL_DIVIDE expression
    | expression INTEGER_DIVIDE expression
    | expression MODULUS expression
    | expression EXPONENT expression'''
    if t[2] == '+':
        t[0] = Plus(t[1], t[3])
    elif t[2] == '-':
        t[0] = Minus(t[1], t[3])
    elif t[2] == '*':
        t[0] = Times(t[1], t[3])
    elif t[2] == '/':
        t[0] = NormalDivide(t[1], t[3])
    elif t[2] == 'div':
        t[0] = IntegerDivide(t[1], t[3])
    elif t[2] == 'mod':
        t[0] = Modulus(t[1], t[3])
    elif t[2] == '**':
        t[0] = Exponent(t[1], t[3])


def p_true(t):
    'expression : TRUE'
    t[0] = AstTrue()


def p_false(t):
    'expression : FALSE'
    t[0] = AstFalse()


# taken from ttgrammer in class
def p_prop_negation(p):
    'expression : NEGATION expression'
    p[0] = Negation(p[2])


def p_prop_conjunction(p):
    'expression : expression CONJUNCTION expression'
    p[0] = Conjunction(p[1], p[3])


def p_prop_disjunction(p):
    'expression : expression DISJUNCTION expression'
    p[0] = Disjunction(p[1], p[3])


# comparison for string and numbers
def p_less_than(p):
    'expression : expression LESS_THAN expression'
    p[0] = LessThan(p[1], p[3])


def p_less_equal(p):
    'expression : expression LESS_EQUAL expression'
    p[0] = LessEqual(p[1], p[3])


def p_prop_not_equal(p):
    'expression : expression NOT_EQUAL expression'
    p[0] = NotEqual(p[1], p[3])


def p_equal_to(p):
    'expression : expression EQUAL_TO expression'
    p[0] = EqualTo(p[1], p[3])


def p_greater_than(p):
    'expression : expression GREATER_THAN expression'
    p[0] = GreaterThan(p[1], p[3])


def p_greater_equal(p):
    'expression : expression GREATER_EQUAL expression'
    p[0] = GreaterEqual(p[1], p[3])


# string, tuples and lists~~~~~~~~~~~~~~~~~~~~~
def p_comma_elements(p):
    '''comma_elements : expression
    | expression COMMA comma_elements'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[3].insert(0, p[1])
        p[0] = p[3]


def p_sbml_list(p):
    '''expression : OPEN_INDEXING CLOSE_INDEXING
    | OPEN_INDEXING comma_elements CLOSE_INDEXING'''
    if len(p) == 4:
        p[0] = AstList(p[2])
    elif len(p) == 3:
        p[0] = AstList(0)


def p_string(p):
    'expression : STRING'
    p[0] = AstString(p[1])


def p_tuple(p):
    'expression : LEFT_PARENTHESIS comma_elements RIGHT_PARENTHESIS'
    if len(p) == 4:
        p[0] = AstTuple(p[2], False)
    else:
        p[0] = AstTuple(p[2], True)


def p_indexing(p):
    'expression : expression OPEN_INDEXING expression CLOSE_INDEXING'
    p[0] = Indexing(p[1], p[3])


# need to change
def p_tuple_indexing(p):
    'expression : TUPLE_INDEXING expression LEFT_PARENTHESIS comma_elements RIGHT_PARENTHESIS'
    p[0] = TupleIndexing(p[2], p[4])


def p_membership(p):
    '''expression : expression MEMBERSHIP OPEN_INDEXING comma_elements CLOSE_INDEXING
    | expression MEMBERSHIP expression'''
    if len(p) == 6:
        p[0] = Membership(p[1], p[4], True)
    else:
        p[0] = Membership(p[1], p[3], True)


def p_cons(p):
    'expression : expression CONS expression'
    p[0] = Cons(p[1], p[3])


# error case
def p_error(t):
    return None


import ply.yacc as yacc

parser = yacc.yacc(debug=0)


def parse(inp):
    # result = parser.parse(inp, debug = 1)
    result = parser.parse(inp, debug=0)
    return result


def main():
    # taken from slides

    f = open(sys.argv[1], "r")
    line = f.readline()
    blockCode = ""
    while line:
        blockCode += line
        line = f.readline()
    f.close()

    result = parse(blockCode)
    if result != None:
        if (result.typecheck() != "Semantic Error"):
            res = result.eval()
            if res == "Semantic Error":
                print("SEMANTIC ERROR")
            else:
                pass
        else:
            print("SEMANTIC ERROR")
    else:
        print("SYNTAX ERROR")


if __name__ == "__main__":
    main()



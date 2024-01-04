import math


# Base Expression Class
class Expr:
    def __add__(self, other):
        if isinstance(other, (int, float)):
            other = Con(other)
        return Add(self, other)

    def __sub__(self, other):
        if isinstance(other, (int, float)):
            other = Con(other)
        return Sub(self, other)

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            other = Con(other)
        return Mul(self, other)

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            other = Con(other)
        return Div(self, other)

    def __neg__(self):
        return Neg(self)

    def simplify(self):
        return self


# Constant Class
class Con(Expr):
    def __init__(self, val):
        self.val = val

    def __str__(self):
        return str(self.val)

    def ev(self, env):
        return self

    def diff(self, name):
        return Con(0)

    def simplify(self):
        return self


# Variable Class
class Var(Expr):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def ev(self, env):
        return Con(env[self.name])

    def diff(self, name):
        return Con(1 if self.name == name else 0)

    def simplify(self):
        return self


# Binary Operation Abstract Class
class BinOp(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return f"({self.left} {self.name} {self.right})"


# Addition Class
class Add(BinOp):
    name = "+"

    def ev(self, env):
        return Con(self.left.ev(env).val + self.right.ev(env).val)

    def diff(self, name):
        return Add(self.left.diff(name), self.right.diff(name))

    def simplify(self):
        left = self.left.simplify()
        right = self.right.simplify()
        if isinstance(left, Con) and left.val == 0:
            return right
        if isinstance(right, Con) and right.val == 0:
            return left
        if isinstance(left, Con) and isinstance(right, Con):
            return Con(left.val + right.val)
        if right == Con(0):
            return left
        if left == Con(0):
            return right
        return Add(left, right)


# Subtraction Class
class Sub(BinOp):
    name = "-"

    def ev(self, env):
        return Con(self.left.ev(env).val - self.right.ev(env).val)

    def diff(self, name):
        return Sub(self.left.diff(name), self.right.diff(name))

    def simplify(self):
        left = self.left.simplify()
        right = self.right.simplify()
        if isinstance(left, Con) and left.val == 0:
            return Neg(right)
        if isinstance(left, Con) and isinstance(right, Con):
            return Con(left.val - right.val)
        if right == Con(0):
            return left
        if left == right:
            return Con(0)
        return Sub(left, right)


# Multiplication Class
class Mul(BinOp):
    name = "*"

    def ev(self, env):
        return Con(self.left.ev(env).val * self.right.ev(env).val)

    def diff(self, name):
        return Add(Mul(self.left.diff(name), self.right), Mul(self.left, self.right.diff(name)))

    def simplify(self):
        left = self.left.simplify()
        right = self.right.simplify()
        if isinstance(left, Con):
            if left.val == 0:
                return Con(0)
            if left.val == 1:
                return right

        if isinstance(right, Con):
            if right.val == 0:
                return Con(0)
            if right.val == 1:
                return left

        if isinstance(right, Con) and right.val == -1:
            return Neg(left)

        if isinstance(left, Con) and isinstance(right, Con):
            return Con(left.val * right.val)
        if left == Con(0) or right == Con(0):
            return Con(0)
        if left == Con(1):
            return right
        if right == Con(1):
            return left
        return Mul(left, right)


# Division Class
class Div(BinOp):
    name = "/"

    def ev(self, env):
        return Con(self.left.ev(env).val / self.right.ev(env).val)

    def diff(self, name):
        return Div(Sub(Mul(self.left.diff(name), self.right), Mul(self.left, self.right.diff(name))), Mul(self.right, self.right))

    def simplify(self):
        left = self.left.simplify()
        right = self.right.simplify()
        if isinstance(left, Con) and isinstance(right, Con) and right.val != 0:
            return Con(left.val / right.val)
        if left == right:
            return Con(1)
        if right == Con(1):
            return left
        if left == Con(0):
            return Con(0)
        return Div(left, right)


# Negation Class
class Neg(Expr):
    def __init__(self, expr):
        self.expr = expr

    def __str__(self):
        return f"(-{self.expr})"

    def ev(self, env):
        return Con(-self.expr.ev(env).val)

    def diff(self, name):
        return Neg(self.expr.diff(name))

    def simplify(self):
        expr = self.expr.simplify()
        if isinstance(expr, Neg):
            # Simplify the inner expression of the nested Neg
            return expr.expr.simplify()
        if isinstance(expr, Con):
            return Con(-expr.val)
        if isinstance(expr, Neg):  # Simplify double negation
            return expr.expr
        return Neg(expr)


# Exponential Class
class Exp(Expr):
    def __init__(self, expr):
        self.expr = expr

    def __str__(self):
        return f"exp({self.expr})"

    def ev(self, env):
        return Con(math.exp(self.expr.ev(env).val))

    def diff(self, name):
        return Mul(Exp(self.expr), self.expr.diff(name))

    def simplify(self):
        expr = self.expr.simplify()
        if isinstance(expr, Con):
            return Con(math.exp(expr.val))
        if isinstance(expr, Neg):  # Simplify exp(-x) to 1/exp(x)
            return Con(1) / Exp(expr.expr)
        return Exp(expr)


# Test Examples
env = {"x": 2}

expr1 = Div(Con(1), Add(Exp(Neg(Var("x"))), Con(1)))  # 1 / (exp(-x) + 1)
expr2 = Div(Sub(Exp(Var("x")), Exp(Neg(Var("x")))), Add(Exp(Var("x")), Exp(Neg(Var("x")))))  # (exp(x) - exp(-x))/(exp(x) + exp(-x))

print("Expression 1:", expr1)
print("Simplified Expression 1:", expr1.simplify())
print("Evaluated Expression 1:", expr1.ev(env))

print("Expression 2:", expr2)
print("Simplified Expression 2:", expr2.simplify())
print("Evaluated Expression 2:", expr2.ev(env))

# Differentiating the test expressions
diff_expr1 = expr1.diff("x").simplify()  # Differentiating and simplifying expression 1
diff_expr2 = expr2.diff("x").simplify()  # Differentiating and simplifying expression 2

# Printing the differentiated expressions
print("Differentiated Expression 1:", diff_expr1)
print("Differentiated Expression 2:", diff_expr2)
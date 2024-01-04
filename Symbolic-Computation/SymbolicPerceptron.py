import math
import numpy as np


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


def linear(xs):
    s = Var("w0")  # bias
    for i, x in enumerate(xs):
        s = s + Var(f"w{i+1}") * Con(x)
    return s


def sigmoid(xs):
    s = Var("w0")  # bias
    for i, x in enumerate(xs):
        s = s + Var(f"w{i+1}") * Con(x)
    return Con(1) / (Exp(-s) + 1)


class P():
    def __init__(self, ninp, sigma, weights=None):
        self.ninp = ninp
        self.sigma = sigma
        self.weights = {}
        vals = weights if weights is not None else (np.random.rand(self.ninp + 1) - 1) / 10
        for i in range(self.ninp + 1):
            self.weights[f"w{i}"] = vals[i]

    def output(self, inp):
        activation_expr = self.sigma(inp)
        return activation_expr.ev(self.weights).val

    def loss(self, dataset):
        err = 0
        for inp, target in dataset:
            predicted_output = self.output(inp)
            error = target - predicted_output
            err += error ** 2
        return err / (2 * len(dataset))

    def train(self, trainset):
        maxepoch = 100000
        alpha = 1e-3
        for e in range(maxepoch):
            for inp, target in trainset:
                out_expr = self.sigma(inp)
                output = out_expr.ev(self.weights).val

                gradients = {}
                for w in self.weights.keys():
                    partial_deriv = out_expr.diff(w).ev(self.weights).val
                    gradients[w] = 2 * (output - target) * partial_deriv

                for w in self.weights.keys():
                    self.weights[w] -= alpha * gradients[w]

            if e % 10 == 0:
                print(f"epoch {e}: loss = {self.loss(trainset)}")


# Assuming the P class and the activation functions (sigmoid, linear) are already defined

# Define a training dataset
trainset = [
    # Format: ([input1, input2], target)
    ([0.5, -0.6], 1),
    ([-0.3, 0.8], 0),
    ([0.7, -0.4], 1),
    ([0.2, 0.9], 0),
    ([-0.1, -0.5], 1),
    ([0.3, 0.3], 0),
    ([0.6, -0.2], 1),
    ([-0.6, -0.8], 0),
    ([-0.7, 0.6], 1),
    ([0.4, 0.7], 0),
    ([0.1, -0.9], 1),
    ([-0.4, 0.5], 0),
    ([0.8, -0.1], 1),
    ([-0.5, -0.7], 0),
    ([0.9, 0.4], 1),
    ([0.0, 0.0], 0),  # Edge case
    ([1.0, 1.0], 1),  # Edge case
    ([-1.0, -1.0], 0), # Edge case
]



# Create and train a perceptron with the sigmoid activation function
ninp = 2  # Number of inputs
rng = np.random.default_rng()
initial_weights = rng.random(ninp + 1) - 0.5
perceptron = P(ninp, sigmoid, initial_weights)
perceptron.train(trainset)

# Uncomment below lines to use the linear activation function instead
# perceptron = P(ninp, linear, initial_weights)
# perceptron.train(trainset)

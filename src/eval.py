import parse
from math import gcd, lcm
from numpy import real, imag, sqrt, array
from scipy.special import gamma

class ComplexNumberValue:
    def __init__(self, ra, rb, ia, ib):
        self.ra = ra
        self.rb = rb
        self.ia = ia
        self.ib = ib

    def simplify(self):
        gcdr = gcd(self.ra, self.rb)
        self.ra //= gcdr
        self.rb //= gcdr
        gcdi = gcd(self.ia, self.ib)
        self.ia //= gcdi
        self.ib //= gcdi
        return self

    def __repr__(self):
        self.simplify()
        
        # return self.repr_fraction()
        return self.repr_decimal()
    
    def repr_decimal(self):
        if self.ra == 0 and (self.ia / self.ib not in [1,0,-1]):
            return f"{self.ia/self.ib:g}i"

        if self.ra != 0 and (self.ia / self.ib == 1):
            return f"{self.ra/self.rb:g} + i"
        
        if self.ra != 0 and (self.ia / self.ib == -1):
            return f"{self.ra/self.rb:g} - i"
        
        if self.ia == 0:
            return f"{self.ra/self.rb:g}"
        
        if self.ra == 0 and (self.ia / self.ib == 1):
            return "i"
        
        if self.ra == 0 and (self.ia / self.ib == -1):
            return "-i"
        
        if self.ra != 0 and (self.ia / self.ib < -1):
            return f"{self.ra/self.rb:g} - {-self.ia/self.ib:g}i"
        
        return f"{self.ra/self.rb:g} + {self.ia/self.ib:g}i"
    
    def repr_fraction(self):
        if self.ra != 0 and self.rb > 1 and self.ia < -1 and self.ib > 1:
            return f"{self.ra}/{self.rb} - {self.ia}i/{self.ib}"
        
        if self.ra != 0 and self.rb == 1 and self.ia > 1 and self.ib > 1:
            return f"{self.ra} + {self.ia}i/{self.ib}"
        
        if self.ra != 0 and self.rb == 1 and self.ia < -1 and self.ib > 1:
            return f"{self.ra} - {self.ia}i/{self.ib}"
        
        if self.ra != 0 and self.rb > 1 and self.ia > 1 and self.ib == 1:
            return f"{self.ra}/{self.rb} + {self.ia}i"
        
        if self.ra != 0 and self.rb > 1 and self.ia < -1 and self.ib == 1:
            return f"{self.ra}/{self.rb} - {self.ia}i"
        
        if self.ra != 0 and self.rb > 1 and self.ia == 1 and self.ib > 1:
            return f"{self.ra}/{self.rb} + i/{self.ib}"
        
        if self.ra != 0 and self.rb > 1 and self.ia == -1 and self.ib > 1:
            return f"{self.ra}/{self.rb} - i/{self.ib}"
        
        if self.ra != 0 and self.rb > 1 and self.ia == 1 and self.ib == 1:
            return f"{self.ra}/{self.rb} + i"
        
        if self.ra != 0 and self.rb > 1 and self.ia == -1 and self.ib == 1:
            return f"{self.ra}/{self.rb} - i"
        
        if self.ra != 0 and self.rb == 1 and self.ia > 1 and self.ib == 1:
            return f"{self.ra} + {self.ia}i"
        
        if self.ra != 0 and self.rb == 1 and self.ia < -1 and self.ib == 1:
            return f"{self.ra} - {self.ia}i"
        
        if self.ra == 0 and self.ib > 1 and self.ia == 0:
            return f"{self.ia}i/{self.ib}"
        
        if self.ra != 0 and self.rb > 1 and self.ia == 0:
            return f"{self.ra}/{self.rb}"
        
        if self.ra != 0 and self.rb == 1 and self.ia == 1 and self.ib > 1:
            return f"{self.ra} + i/{self.ib}"
        
        if self.ra != 0 and self.rb == 1 and self.ia == -1 and self.ib > 1:
            return f"{self.ra} - i/{self.ib}"
        
        if self.ra != 0 and self.rb == 1 and self.ia == 1 and self.ib == 1:
            return f"{self.ra} + i"
        
        if self.ra != 0 and self.rb == 1 and self.ia == -1 and self.ib == 1:
            return f"{self.ra} - i"
        
        if self.ra == 0 and self.ia > 1 and self.ib == 1:
            return f"{self.ia}i"
        
        if self.rb == 1 and self.ia == 0:
            return f"{self.ra}"
        
        if self.ra == 0 and self.ia == 1 and self.ib == 1:
            return "i"
        
        if self.ra == 0 and self.ia == 1 and self.ib > 1:
            return f"i/{self.ib}"
        
        return f"{self.ra}/{self.rb} + {self.ia}i/{self.ib}"
    
    def __add__(self, other):
        # Real Segment
        if not isinstance(other, ComplexNumberValue):
            raise Exception("cannot add number to non-number value")
        lcmr = lcm(self.rb, other.rb)
        rbf = lcmr
        raf1 = self.ra * (lcmr // self.rb)
        raf2 = other.ra * (lcmr // other.rb)
        raf = raf1 + raf2
        # Imaginary Segment
        lcmi = lcm(self.ib, other.ib)
        ibf = lcmi
        iaf1 = self.ia * (lcmi // self.ib)
        iaf2 = other.ia * (lcmi // other.ib)
        iaf = iaf1 + iaf2
        return ComplexNumberValue(raf, rbf, iaf, ibf).simplify()
    
    def __sub__(self, other):
        # Real Segment
        lcmr = lcm(self.rb, other.rb)
        rbf = lcmr
        raf1 = self.ra * (lcmr // self.rb)
        raf2 = other.ra * (lcmr // other.rb)
        raf = raf1 - raf2
        # Imaginary Segment
        lcmi = lcm(self.ib, other.ib)
        ibf = lcmi
        iaf1 = self.ia * (lcmi // self.ib)
        iaf2 = other.ia * (lcmi // other.ib)
        iaf = iaf1 - iaf2
        return ComplexNumberValue(raf, rbf, iaf, ibf).simplify()
    
    def __mul__(self, other):
        # Real Segment
        raf = self.ra * other.ra * self.ib * other.ib - self.ia * other.ia * self.rb * other.rb
        rbf = self.rb * other.rb * self.ib * other.ib
        iaf = self.ra * other.ia * other.rb * self.ib + other.ra * self.ia * self.rb * other.ib
        ibf = rbf
        return ComplexNumberValue(raf, rbf, iaf, ibf).simplify()
    
    def __truediv__(self, other):
        raf = other.rb * other.ib * (self.ra * other.ra * self.ib * other.ib + self.ia * other.ia * self.rb * other.rb)
        rbf = self.rb * self.ib * (other.ra * other.ra * other.ib * other.ib + other.ia * other.ia * other.rb * other.rb)
        iaf = other.rb * other.ib * (other.ra * self.ia * self.rb * other.ib - self.ra * other.ia * self.ib * other.rb)
        ibf = rbf
        return ComplexNumberValue(raf, rbf, iaf, ibf).simplify()
    
    def __pow__(self, other):
        return apply_function(lambda x, y: x ** y, self, other)
    
    def __neg__(self):
        return ComplexNumberValue(-self.ra, self.rb, -self.ia, self.ib).simplify()
    
    def abs(self):
        return apply_function(abs, self)

class BooleanValue:
    def __init__(self, value: bool):
        self.boolean = value
    
    def __repr__(self):
        return "true" if self.boolean else "false"
    
    def __and__(self, other):
        return BooleanValue(self.boolean and other.boolean)
    
    def __or__(self, other):
        return BooleanValue(self.boolean or other.boolean)
    
    def __xor__(self, other):
        return BooleanValue(self.boolean ^ other.boolean)
    
    def not_gate(self):
        return BooleanValue(not self.boolean)

class FunctionValue:
    def __init__(self, params, expression):
        self.params = params
        self.expression = expression

class EncodedFunctionValue:
    def __init__(self, name, function, param_types):
        self.name = name
        self.function = function
        self.param_domains = param_types

class VectorValue:
    def __init__(self, members):
        self.members = members
    
    def __repr__(self):
        return str(self.members)
    
    def __add__(self, other):
        if not isinstance(other, VectorValue):
            raise Exception("cannot add vector to non-vector value")
        if len(self.members) != len(other.members):
            raise TypeError(f"vector sizes for {self} and {other} do not match")
        new_list = []
        for i in range(len(self.members)):
            new_list.append(self.members[i] + other.members[i])
        return VectorValue(new_list)
    
    def __mul__(self, other):
        if isinstance(other, VectorValue):
            if len(self.members) != len(other.members):
                raise TypeError(f"vector sizes for {self} and {other} do not match")
            dotsum = ComplexNumberValue(0,1,0,1)
            for i in range(len(self.members)):
                dotsum += self.members[i] * other.members[i]
            return dotsum
        if isinstance(other, ComplexNumberValue):
            new_list = []
            for i in range(len(self.members)):
                new_list.append(self.members[i] * other)
            return VectorValue(new_list)
        raise Exception("multiplication undefined")
    
    def abs(self):
        unrooted_square_sum = ComplexNumberValue(0, 1, 0, 1)
        for member in self.members:
            unrooted_square_sum += member * member
        return apply_function(sqrt, unrooted_square_sum)
    
def apply_function(func, *num):
    numbers = [n.ra / n.rb + n.ia / n.ib * 1j for n in num]
    output = func(*numbers)
    return ComplexNumberValue(int(real(output)*1000000000000000), 1000000000000000, int(imag(output)*1000000000000000), 1000000000000000).simplify()

def get_pythonic_value(value):
    if type(value) == ComplexNumberValue:
        re = value.ra / value.rb
        im = value.ia / value.ib
        if re == int(re): re = int(re)
        if im == int(im): im = int(im)
        
        return re if im == 0 else re + im * 1j
    if type(value) == VectorValue:
        return array([get_pythonic_value(member) for member in value.members])

class Evaluator:
    def __init__(self, expression, knowns):
        self.expression = expression
        self.knowns = knowns

    def evaluate(self):
        return self.eval_expr(self.expression)
    
    def eval_expr(self, expression):
        if type(expression) == parse.DefinitionStatement:
            # Functions
            if type(expression.left) == parse.ImplicitExpression:
                # Single Variable Functions
                if type(expression.left.right) == parse.IdentifierExpression:
                    self.knowns[expression.left.left.string] = parse.FunctionExpression([expression.left.right], expression.right)
                # Multivariable Functions
                elif type(expression.left.right) == parse.VectorExpression:
                    self.knowns[expression.left.left.string] = parse.FunctionExpression(expression.left.right.members, expression.right)
            # Variables
            elif type(expression.left) == parse.IdentifierExpression:
                self.knowns[expression.left.string] = expression.right
            else:
                raise Exception("Non-identifier lvalue")
        if type(expression) == parse.AdditionExpression:
            return self.eval_expr(expression.left) + self.eval_expr(expression.right)
        if type(expression) == parse.SubtractionExpression:
            return self.eval_expr(expression.left) - self.eval_expr(expression.right)
        if type(expression) == parse.NegationExpression:
            return -self.eval_expr(expression.expression)
        if type(expression) == parse.FactorialExpression:
            return apply_function(lambda n: gamma(n + 1), self.eval_expr(expression.expression))
        if type(expression) == parse.MultiplicationExpression:
            return self.eval_expr(expression.left) * self.eval_expr(expression.right)
        if type(expression) == parse.DivisionExpression:
            return self.eval_expr(expression.left) / self.eval_expr(expression.right)
        if type(expression) == parse.ExponentExpression:
            return self.eval_expr(expression.left) ** self.eval_expr(expression.right)
        if type(expression) == parse.AbsoluteExpression:
            return self.eval_expr(expression.expression).abs()
        if type(expression) == parse.AndExpression:
            return self.eval_expr(expression.left) and self.eval_expr(expression.right)
        if type(expression) == parse.OrExpression:
            return self.eval_expr(expression.left) or self.eval_expr(expression.right)
        if type(expression) == parse.XorExpression:
            return self.eval_expr(expression.left) ^ self.eval_expr(expression.right)
        if type(expression) == parse.NotExpression:
            return self.eval_expr(expression.expression).not_gate()
        if type(expression) == parse.ImplicitExpression:
            lvalue = self.eval_expr(expression.left)
            if type(lvalue) == ComplexNumberValue:
                return lvalue * self.eval_expr(expression.right)
            if type(lvalue) == FunctionValue:
                expr = lvalue.expression
                for i, param in enumerate(lvalue.params):
                    expr = parse.sub(expr, param, expression.right if len(lvalue.params) == 1 else expression.right.members[i])
                return self.eval_expr(expr)
            if type(lvalue) == EncodedFunctionValue:
                if len(lvalue.param_domains) == 1:
                    rvalue = self.eval_expr(expression.right)
                    value = get_pythonic_value(rvalue)
                    if not lvalue.param_domains[0](value):
                        raise Exception("types do not match")
                    try:
                        output = lvalue.function(value)
                        return ComplexNumberValue(int(real(output)*1000000000000000), 1000000000000000, int(imag(output)*1000000000000000), 1000000000000000).simplify()
                    except ValueError as e:
                        raise e
                else:
                    if type(expression.right) != VectorValue or len(expression.right) != len(lvalue.param_domains):
                        raise Exception("unhandled number of arguments")
                    rvalues = []
                    for member in expression.right.members:
                        rvalues.append(self.eval_expr(member))
                    values = [get_pythonic_value(rvalue) for rvalue in rvalues]
                    for i in range(len(lvalue.param_domains)):
                        if not lvalue.param_domains[i](values[i]):
                            raise Exception("types do not match")
                    try:
                        return ComplexNumberValue(int(lvalue.function(*values)*1000000000000000), 1000000000000000, 0, 1).simplify()
                    except ValueError as e:
                        raise e
        if type(expression) == parse.FunctionExpression:
            return FunctionValue(expression.params, expression.expression)
        if type(expression) == parse.EncodedFunctionExpression:
            return EncodedFunctionValue(expression.name, expression.function, expression.param_types)
        if type(expression) == parse.VectorExpression:
            return VectorValue([self.eval_expr(member) for member in expression.members])
        if type(expression) == parse.NumberExpression:
            return ComplexNumberValue(expression.dividend, expression.divisor, 0, 1).simplify()
        if type(expression) == parse.ImaginaryExpression:
            return ComplexNumberValue(0, 1, 1, 1)
        if type(expression) == parse.BooleanExpression:
            return BooleanValue(expression.boolean)
        if type(expression) == parse.IdentifierExpression:
            if expression.string in list(self.knowns):
                return self.eval_expr(self.knowns[expression.string])
            raise Exception(f"identifier \"{expression.string}\" is undefined")

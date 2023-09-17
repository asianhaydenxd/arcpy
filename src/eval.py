import parse
from math import gcd
from numpy import real, imag

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
        if self.ra != 0 and self.ia < -1:
            return f"{self.ra/self.rb:g} - {self.ia/self.ib:g}i"
        
        if self.ra == 0 and (self.ia > 1 or self.ia < -1) and self.ib == 1:
            return f"{self.ia/self.ib:g}i"

        if self.ra != 0 and self.ia == 1:
            return f"{self.ra/self.rb:g} + i"
        
        if self.ra != 0 and self.ia < -1:
            return f"{self.ra/self.rb:g} - {self.ia/self.ib:g}i"
        
        if self.ra != 0 and self.ia == -1:
            return f"{self.ra/self.rb:g} - i"
        
        if self.ia == 0:
            return f"{self.ra/self.rb:g}"
        
        if self.ra == 0 and (self.ia > 1 or self.ia < -1):
            return f"{self.ia/self.ib:g}i"
        
        if self.ra == 0 and self.ia == 1:
            return "i"
        
        if self.ra == 0 and self.ia == -1:
            return "-i"
        
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
        lcm = self.rb * gcd(self.rb, other.rb) // other.rb;
        rbf = lcm;
        raf1 = self.ra * (lcm // self.rb);
        raf2 = other.ra * (lcm // other.rb);
        raf = raf1 + raf2;
        # Imaginary Segment
        lcmi = self.ib * gcd(self.ib, other.ib) // other.ib;
        ibf = lcmi;
        iaf1 = self.ia * (lcmi // self.ib);
        iaf2 = other.ia * (lcmi // other.ib);
        iaf = iaf1 + iaf2;
        return ComplexNumberValue(raf, rbf, iaf, ibf).simplify()
    
    def __sub__(self, other):
        # Real Segment
        lcm = self.rb * gcd(self.rb, other.rb) // other.rb
        rbf = lcm
        raf1 = self.ra * (lcm // self.rb)
        raf2 = other.ra * (lcm // other.rb)
        raf = raf1 - raf2
        # Imaginary Segment
        lcmi = self.ib * gcd(self.ib, other.ib) // other.ib
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
        raf = other.rb * other.ib * (self.ra * other.ra * self.ib * other.ib + self.ia * other.ia * self.rb * other.rb);
        rbf = self.rb * self.ib * (other.ra * other.ra * other.ib * other.ib + other.ia * other.ia * other.rb * other.rb);
        iaf = other.rb * other.ib * (other.ra * self.ia * self.rb * other.ib + self.ra * other.ia * self.ib * other.rb);
        ibf = rbf;
        return ComplexNumberValue(raf, rbf, iaf, ibf).simplify()
    
    def __neg__(self):
        return ComplexNumberValue(-self.ra, self.rb, -self.ia, self.ib).simplify()

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
        if len(self.members) != len(other.members):
            raise TypeError(f"vector sizes for {self} and {other} do not match")
        new_list = []
        for i in range(len(self.members)):
            new_list.append(self.members[i] + other.members[i])
        return VectorValue(new_list)
    
def apply_function(func, *num):
    numbers = [n.ra / n.rb + n.ia / n.ib * 1j for n in num]
    output = func(*numbers)
    return ComplexNumberValue(int(real(output)*1000000000000000), 1000000000000000, int(imag(output)*1000000000000000), 1000000000000000).simplify()

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
        if type(expression) == parse.MultiplicationExpression:
            return self.eval_expr(expression.left) * self.eval_expr(expression.right)
        if type(expression) == parse.DivisionExpression:
            return self.eval_expr(expression.left) / self.eval_expr(expression.right)
        if type(expression) == parse.ExponentExpression:
            return apply_function(lambda x, y: x ** y, self.eval_expr(expression.left), self.eval_expr(expression.right))
        if type(expression) == parse.AbsoluteExpression:
            return apply_function(abs, self.eval_expr(expression.expression))
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
                    number = rvalue.ra / rvalue.rb if rvalue.ia == 0 else rvalue.ra / rvalue.rb + rvalue.ia / rvalue.ib * 1j
                    if not lvalue.param_domains[0](number):
                        raise Exception("types do not match")
                    try:
                        output = lvalue.function(number)
                        return ComplexNumberValue(int(real(output)*1000000000000000), 1000000000000000, int(imag(output)*1000000000000000), 1000000000000000).simplify()
                    except ValueError as e:
                        raise e
                else:
                    rvalues = []
                    for member in expression.right.members:
                        rvalues.append(self.eval_expr(member))
                    numbers = [rvalue.ra / rvalue.rb if rvalue.ia == 0 else rvalue.ra / rvalue.rb + rvalue.ia / rvalue.ib * 1j for rvalue in rvalues]
                    for i in range(len(lvalue.param_domains)):
                        if not lvalue.param_domains[i](numbers[i]):
                            raise Exception("types do not match")
                    try:
                        return ComplexNumberValue(int(lvalue.function(*numbers)*1000000000000000), 1000000000000000, 0, 1).simplify()
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
        if type(expression) == parse.IdentifierExpression:
            if expression.string in list(self.knowns):
                return self.eval_expr(self.knowns[expression.string])

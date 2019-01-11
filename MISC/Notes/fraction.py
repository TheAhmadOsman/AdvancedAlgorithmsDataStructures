class Fraction:
    def __init__(self, top=0, bottom=1):
        divisor = Fraction.gcd(top, bottom)
        self.top = top // divisor
        self.bottom = bottom // divisor

    def gcd(a, b):
        if b == 0:
            return a
        return Fraction.gcd(b, a % b)

    def __add__(self, other):
        denominator = self.bottom * other.bottom
        numerator = (self.bottom * other.top) + (other.bottom * self.top)
        return Fraction(numerator, denominator)

    def __str__(self):
        return str(self.top) + "/" + str(self.bottom)


def main():
    x = Fraction(4, 9)
    y = Fraction(5, 13)
    print(x + y)

    a = Fraction(4, 12)
    b = Fraction(2, 3)
    c = a + b
    print(c)


if __name__ == "__main__":
    main()

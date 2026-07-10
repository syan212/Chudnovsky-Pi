from functools import lru_cache
from decimal import Decimal, getcontext
from sys import exit

factorials = [
    1,
    1,
    2,
    6,
    24,
    120,
    720,
    5040,
    40320,
    362880,
    3628800,
    39916800,
    479001600,
    6227020800,
    87178291200,
    1307674368000,
    20922789888000,
    355687428096000,
    6402373705728000,
    121645100408832000,
    2432902008176640000,
    51090942171709440000,
    1124000727777607680000,
    25852016738884976640000,
    620448401733239439360000,
    15511210043330985984000000,
    403291461126605635584000000,
    10888869450418352160768000000,
    304888344611713860501504000000,
    8841761993739701954543616000000,
    265252859812191058636308480000000,
]


@lru_cache
def factorial(n: int) -> int:
    if n == 0:
        return 1
    elif n < 30:
        return factorials[n]
    else:
        return n * factorial(n - 1)


def chudnovsky(it: int) -> Decimal:
    sum = Decimal(0)
    for i in range(it):
        numerator = factorial(6 * i) * (545140134 * i + 13591409)
        denominator = factorial(3 * i) * factorial(i) ** 3 * 640320 ** (3 * i)
        n = Decimal(numerator) / Decimal(denominator)
        if i % 2 == 1:
            sum -= n
        else:
            sum += n
    return Decimal(1) / (sum * Decimal(10005).sqrt() / Decimal(4270934400))


def main():
    try:
        iterations = int(input("How many iterations of the Chudnovsky Algorithm? : "))
        prec = int(
            input("What precision do you want to use? (in d.p., 1,000,000 max): ")
        )
    except ValueError:
        print("Input(s) need to be positive integers. Aborting program")
        exit()
    getcontext().prec = int(prec)
    pi = chudnovsky(iterations)
    print(pi)


if __name__ == "__main__":
    main()

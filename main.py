from decimal import Decimal, getcontext
from functools import lru_cache
from sys import exit

from compression import zstd
from rich import print as rprint

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
    8222838654177922817725562880000000,
    263130836933693530167218012160000000,
    8683317618811886495518194401280000000,
    295232799039604140847618609643520000000,
    10333147966386144929666651337523200000000,
    371993326789901217467999448150835200000000,
    13763753091226345046315979581580902400000000,
    523022617466601111760007224100074291200000000,
    20397882081197443358640281739902897356800000000,
    815915283247897734345611269596115894272000000000,
    33452526613163807108170062053440751665152000000000,
    1405006117752879898543142606244511569936384000000000,
    60415263063373835637355132068513997507264512000000000,
    2658271574788448768043625811014615890319638528000000000,
    119622220865480194561963161495657715064383733760000000000,
    5502622159812088949850305428800254892961651752960000000000,
    258623241511168180642964355153611979969197632389120000000000,
    12413915592536072670862289047373375038521486354677760000000000,
    608281864034267560872252163321295376887552831379210240000000000,
    30414093201713378043612608166064768844377641568960512000000000000,
]


@lru_cache
def factorial(n: int) -> int:
    if n == 0:
        return 1
    if n < len(factorials):
        return factorials[n]
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


def main() -> None:
    # Load 1 million digits of pi
    with zstd.open('pi.txt.zst', 'rt') as f:
        correct_pi = f.read()

    try:
        iterations = int(input('How many iterations of the Chudnovsky Algorithm? : '))
        prec = int(
            input('What precision do you want to use? (in d.p., 1,000,000 max): ')
        )
    except ValueError:
        rprint('[red]Input(s) need to be positive integers. Aborting program.')
        exit()
    getcontext().prec = int(prec)
    pi = chudnovsky(iterations)
    num_correct = 0

    for i, char in enumerate(str(pi)[2:]):
        if char != correct_pi[i + 2]:
            break
        num_correct += 1
    rprint(
        f'[yellow][b]{num_correct}[/b] digits of pi (after the decimal point) were calculated correctly[/yellow]'
    )
    print('Calculated result (green is correct digits, red is incorrect):')
    rprint(
        f'[green]{str(pi)[: num_correct + 2]}[/green][red]{str(pi)[num_correct + 2 :]}[/red]'
    )


if __name__ == '__main__':
    main()

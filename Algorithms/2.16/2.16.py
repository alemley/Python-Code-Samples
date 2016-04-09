import math


def main():
    n = [10, 20, 40, 80, 160, 320]
    p = [1, 2, 4, 8, 16, 32, 64, 128]
    print('Part a)')
    print('Speedup)')
    for i in range(len(p)):
        for j in range(len(n)):
            print('Elements:', n[j])
            print('Processors:', p[i])
            print('Speedup:', speedup(n[j], p[i]), '\n------------------------------')

    print('\n\n\n(Efficiency)')
    for i in range(len(p)):
        for j in range(len(n)):
            print('Elements:', n[j])
            print('Processors:', p[i])
            print('Efficiency:', efficiency_part_a(n[j], p[i]), '\n------------------------------')

    print('\n\n\nPart b)')
    print('Show that if T overhead grows more slowly than Tserial , the parallel efficiency will increase as we '
          'increase the problem size.')
    print('Overhead = n)')
    for i in range(len(p)):
        for j in range(len(n)):
            print('Elements:', n[j])
            print('Processors:', p[i])
            print('Speedup:', efficiency_part_b(n[j], p[i], n[j]), '\n------------------------------')
    print('\n\n\nShow that if, on the other hand, Toverhead grows faster than Tserial , the parallel efficiency will '
          'decrease as we increase the problem size.')
    print('(Overhead = n^3)')
    for i in range(len(p)):
        for j in range(len(n)):
            print('Elements:', n[j])
            print('Processors:', p[i])
            print('Efficiency:', efficiency_part_b(n[j], p[i], ((n[j])**3)), '\n------------------------------')


def serial_time(n):
    return n**2


def parallel_time_part_a(n, p):
    return serial_time(n)/p + math.log(p)/math.log(2)


def parallel_time_part_b(n, p, overhead_time):
    return serial_time(n)/p + overhead_time


def speedup(n, p):
    return serial_time(n) / parallel_time_part_a(n, p)


def efficiency_part_a(n, p):
    return serial_time(n)/(p*parallel_time_part_a(n, p))


def efficiency_part_b(n, p, overhead_time):
    return serial_time(n)/(p*parallel_time_part_b(n, p, overhead_time))


if __name__ == "__main__":
    main()
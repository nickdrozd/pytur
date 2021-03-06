from generate import yield_programs, print_programs

HALT = 0

REJECTS = [
    '^1RB ... ..[BC] ..[BC] ..[BC] ..[BC]',
    '^1RB ..[AB] ..[AB] ..[AB] ... ...',
]

if __name__ == '__main__':
    print_programs(
        yield_programs(
            3,
            2,
            HALT,
            rejects=REJECTS))

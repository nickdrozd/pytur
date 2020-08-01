import argparse
from contextlib import contextmanager

########################################

STATE_MAP = {
    'A': '0',
    'B': '1',
    'C': '2',
    'D': '3',
    'E': '4',
    'F': '5',
    'G': '6',
    'H': '7',
}

HALT = 7

SHIFT_MAP = {
    'L': 0,
    'R': 1,
}

def parse(program_string):
    instructions = iter([
        instr.replace(
            instr[2],
            STATE_MAP[instr[2]])
        for instr in
        program_string.split()
    ])

    return tuple(
        tuple(
            (int(action[0]), int(SHIFT_MAP[action[1]]), int(action[2]))
            for action in instr)
        for instr in
        zip(instructions, instructions)
    )

########################################

class Machine:
    def __init__(self, prog):
        self._prog = parse(prog)
        self._tape = None
        self._pos = None
        self._state = None
        self._exec_count = None

    @property
    def exec_count(self):
        return self._exec_count

    @property
    def ones_count(self):
        return sum(self._tape)

    def run_to_halt(self, tape):
        pos = 0
        state = 0
        exec_count = 0

        prog = self._prog

        while state != HALT:
            (color, shift, state) = prog[state][tape[pos]]

            tape[pos] = color

            if shift:
                pos += 1

                try:
                    tape[pos]
                except IndexError:
                    tape.append(0)

            else:
                if pos == 0:
                    tape.insert(0, 0)
                else:
                    pos -= 1

            exec_count += 1

        self._pos = pos
        self._tape = tape
        self._exec_count = exec_count

    def print_results(self):
        squares = [
            '_' if square == 0 else '#'
            for square in self._tape
        ]

        with_pos = ''.join([
            f'[{square}]' if i == self._pos else square
            for i, square in enumerate(squares)
        ])

        print(
            '\n** {} ** {} ** {}'.format(
                self.ones_count,
                self.exec_count,
                with_pos))

########################################

BB3 = "1RB   1RH   1LB   0RC   1LC   1LA"
BB4 = "1RB   1LB   1LA   0LC   1RH   1LD   1RD   0RA"
TM5 = "1RB   0LC   1RC   1RD   1LA   0RB   0RE   1RH   1LC   1RA"
BB5 = "1RB   1LC   1RC   1RB   1RD   0LE   1LA   1LD   1RH   0LA"


def run_bb(prog):
    machine = Machine(prog)
    machine.run_to_halt([0])
    machine.print_results()


@contextmanager
def profile():
    try:
        import yappi

        yappi.set_clock_type('cpu')
        yappi.start()

        yield

    finally:
        stats = yappi.get_func_stats()
        stats.save('yappi.callgrind', type='callgrind')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--profile')
    args = parser.parse_args()

    if args.profile:
        with profile():
            run_bb(TM5)
    else:
        run_bb(TM5)


    # import yappi

    # yappi.set_clock_type('cpu')
    # yappi.start()

    # run_bb(TM5)

    # stats = yappi.get_func_stats()
    # stats.save('yappi.callgrind', type='callgrind')

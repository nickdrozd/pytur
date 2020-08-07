from collections import defaultdict

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
        self._beep_count = None

    @property
    def exec_count(self):
        return self._exec_count

    @property
    def ones_count(self):
        return sum(self._tape)

    @property
    def beep_count(self):
        return sorted(
            tuple(
                (key, val)
                for key, val in
                self._beep_count.items()),
            key=lambda x: x[1],
            reverse=True)

    def run_to_halt(self, tape):
        pos = 0
        state = 0

        exec_count = 0
        beep_count = defaultdict(lambda: 0)
        prog = self._prog

        for _ in range(10000):
            old_state = state

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
            beep_count[old_state] = exec_count

        self._pos = pos
        self._tape = tape
        self._exec_count = exec_count

        self._beep_count = dict(beep_count)

    def print_results(self, print_tape=False):
        print('\n'.join([
            f'ones: {self.ones_count}',
            f'exec: {self.exec_count}',
            f'beep: {self.beep_count}',
            '',
        ]))

        if print_tape:
            self.print_tape(self._tape, self._pos)

    def print_tape(self, tape, pos):
        squares = [
            '_' if square == 0 else '#'
            for square in tape
        ]

        with_pos = ''.join([
            f'[{square}]' if i == pos else square
            for i, square in enumerate(squares)
        ])

        print(with_pos)

########################################

MACHINES = {
    'BB2': "1RB   1LB   1LA   1RH",
    'BB3': "1RB   1RH   1LB   0RC   1LC   1LA",
    'BB4': "1RB   1LB   1LA   0LC   1RH   1LD   1RD   0RA",
    'TM5': "1RB   0LC   1RC   1RD   1LA   0RB   0RE   1RH   1LC   1RA",
    'BB5': "1RB   1LC   1RC   1RB   1RD   0LE   1LA   1LD   1RH   0LA",
}

BB2 = MACHINES['BB2']
BB3 = MACHINES['BB3']
BB4 = MACHINES['BB4']
TM5 = MACHINES['TM5']
BB5 = MACHINES['BB5']

def run_bb(prog):
    machine = Machine(prog)
    machine.run_to_halt([0])
    return machine

########################################

CANDIDATES = [
    # # BBB(3) = 55
    # "1LB 0RB 1RA 0LC 1RC 1RA",

    # BBB(4) = 2568 ???
    "1RD 1RA 1LB 1LD 0RB 1RA 0RC 0RD",
]


if __name__ == '__main__':
    for i, prog in enumerate(CANDIDATES):
        machine = run_bb(prog)
        # print(f'{i} | {prog.strip()} | {machine.beep_count}')
        machine.print_results()

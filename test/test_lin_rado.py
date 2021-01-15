# pylint: disable = attribute-defined-outside-init

from unittest import TestCase

from turing import run_bb
from generate.generate import yield_programs


class TestLinRado(TestCase):
    def assert_progs_equal(self, other):
        self.assertEqual(
            self.progs,
            other)

    def assert_progs_count(self, count):
        self.assertEqual(
            len(self.progs),
            count)

    def run_lin_rado(self, states, colors, halt, x_limit, rejects=None):
        print(f'{states} {colors} {halt}')

        self.progs = {
            prog
            for prog in
            yield_programs(
                states,
                colors,
                halt,
                rejects=rejects)
            if
            run_bb(
                prog,
                x_limit=x_limit,
                check_rec=0
            ).final[0] == 'XLIMIT'
        }

    def test_22h(self):
        self.run_lin_rado(2, 2, 1, 50)

        self.assert_progs_count(0)

    def test_22q(self):
        self.run_lin_rado(2, 2, 0, 50)

        self.assert_progs_count(4)

        self.assert_progs_equal(
            HOLDOUTS_22Q)

    def test_32h(self):
        self.run_lin_rado(
            3, 2, 1, 50,
            NOT_CONNECTED_32)

        self.assert_progs_count(40)

        self.assert_progs_equal(
            HOLDOUTS_32H)

    def test_32q(self):
        self.run_lin_rado(
            3, 2, 0, 126,
            [AB_LOOP] + [
                prog.replace('1RH', '...')
                for prog in HOLDOUTS_32H
            ])

        self.assert_progs_equal(
            HOLDOUTS_32Q)

        self.assert_progs_count(837)


HOLDOUTS_22Q = {
    "1RB 0LB 1LA 0RA",
    "1RB 1LA 0LA 0RB",
    "1RB 1LA 0LA 1RB",
    "1RB 1LA 1LA 1RB",
}

LR_HOLDOUTS = {
    # Lot 1
    0o73037233,
    0o73137233,
    0o73137123,
    0o73136523,
    0o73133271,
    0o73133251,
    0o73132742,
    0o73132542,
    0o73032532,
    0o73032632,
    0o73033132,
    0o73033271,
    0o73073271,
    0o73075221,
    # Lot 2
    0o73676261,
    0o73736122,
    0o71536037,
    0o73336333,
    0o71676261,
    0o73336133,
    0o73236333,
    0o73236133,
    # Lot 3
    0o70537311,
    0o70636711,
    0o70726711,
    0o72737311,
    0o71717312,
    0o72211715,
    0o72237311,
    0o72311715,
    0o72317716,
    0o72331715,
    0o72337311,
    0o72337315,
    # Lot 4
    0o70513754,
    0o70612634,
    0o70712634,
    0o72377034,
    0o72377234,
    0o72613234,
}


def lr_convert(rado_string):
    def oct_to_bin(oct_string):
        return '{0:b}'.format(oct_string)

    def bin_to_prog(bin_string):
        instrs = [
            bin_string[i : i + 4]
            for i in range(0, len(bin_string), 4)
        ]

        return ' '.join(map(convert_bin_instr, instrs))

    def convert_bin_instr(bin_instr):
        pr, sh, *tr =  bin_instr

        tr = int(''.join(tr), 2)

        return '{}{}{}'.format(
            pr,
            'L' if int(sh) == 0 else 'R',
            'H' if tr == 0 else chr(tr + 64),
        )

    return bin_to_prog(
        oct_to_bin(
            rado_string))


HOLDOUTS_32H = set(map(lr_convert, LR_HOLDOUTS))

AB_LOOP = '^1RB ..[AB] ..[AB] ..[AB] ... ...'
BC_LOOP = '^1RB ... ..[BC] ..[BC] ..[BC] ..[BC]'

NOT_CONNECTED_32 = [
    AB_LOOP,
    BC_LOOP,
]

HOLDOUTS_32Q = {
    "1RB 0LA 1LB 0RC 1LA 1RC",
    "1RB 0LA 1LC 0RA 1LA 0LB",
    "1RB 0LA 1LC 0RB 1RA 1LA",
    "1RB 0LA 1LC 1RC 1LA 0RC",
    "1RB 0LA 1RC 1LB 0LB 0RA",
    "1RB 0LB 0LC 0LA 1RC 1LB",
    "1RB 0LB 0LC 0RC 1RA 1LA",
    "1RB 0LB 0LC 1RA 1LA 1LC",
    "1RB 0LB 0LC 1RA 1RA 1LC",
    "1RB 0LB 0LC 1RA 1RB 1LC",
    "1RB 0LB 0LC 1RC 1RA 1LC",
    "1RB 0LB 0RC 1LA 1LB 1RC",
    "1RB 0LB 0RC 1LB 1LA 1RC",
    "1RB 0LB 0RC 1RB 1LC 0LA",
    "1RB 0LB 0RC 1RC 1LA 1RB",
    "1RB 0LB 0RC 1RC 1LA 1RC",
    "1RB 0LB 1LA 0LC 0RA 1RC",
    "1RB 0LB 1LA 0RC 1LC 1RB",
    "1RB 0LB 1LA 0RC 1RC 0RA",
    "1RB 0LB 1LA 1LC 0RA 1RC",
    "1RB 0LB 1LA 1RC 0LC 0RA",
    "1RB 0LB 1LB 1RC 1RA 1LC",
    "1RB 0LB 1LC 0RA 0RB 1LB",
    "1RB 0LB 1LC 0RA 1LA 0LC",
    "1RB 0LB 1LC 0RC 0LA 1LA",
    "1RB 0LB 1LC 1LB 0LA 1RC",
    "1RB 0LB 1LC 1RA 0RB 0LC",
    "1RB 0LB 1LC 1RA 0RB 1LC",
    "1RB 0LB 1LC 1RA 1LA 1LC",
    "1RB 0LB 1LC 1RA 1RA 1LC",
    "1RB 0LB 1LC 1RA 1RB 1LC",
    "1RB 0LB 1LC 1RC 1LA 1RB",
    "1RB 0LB 1LC 1RC 1RA 1LC",
    "1RB 0LB 1RC 0RA 0LC 1LA",
    "1RB 0LB 1RC 0RB 1LA 0RB",
    "1RB 0LB 1RC 0RB 1LA 1LC",
    "1RB 0LB 1RC 0RC 1LA 0RB",
    "1RB 0LB 1RC 0RC 1LB 1LA",
    "1RB 0LB 1RC 1LB 0LA 0RC",
    "1RB 0LB 1RC 1LC 0LA 0RA",
    "1RB 0LB 1RC 1RB 1LA 1LC",
    "1RB 0LC 0LA 0RA 1RA 1LA",
    "1RB 0LC 0LA 1RA 1LA 0RA",
    "1RB 0LC 0LA 1RA 1LA 1LA",
    "1RB 0LC 0LA 1RA 1RA 1LA",
    "1RB 0LC 0LA 1RB 1LA 1LC",
    "1RB 0LC 0LC 0RA 1LA 0LC",
    "1RB 0LC 0LC 0RA 1LA 1LC",
    "1RB 0LC 0LC 0RA 1LA 1RC",
    "1RB 0LC 0LC 0RB 1RA 1LA",
    "1RB 0LC 0LC 1RA 1LA 0RB",
    "1RB 0LC 0LC 1RC 1RB 1LA",
    "1RB 0LC 0RC 0RB 1LC 1RA",
    "1RB 0LC 0RC 1RA 0LC 1LA",
    "1RB 0LC 1LA 0RA 1RC 1LA",
    "1RB 0LC 1LA 0RC 1LA 0LA",
    "1RB 0LC 1LA 0RC 1LA 0LC",
    "1RB 0LC 1LA 0RC 1LA 1RB",
    "1RB 0LC 1LA 0RC 1LB 0RA",
    "1RB 0LC 1LA 0RC 1RA 0LB",
    "1RB 0LC 1LA 1RA 0RA 0LA",
    "1RB 0LC 1LA 1RA 0RA 0LC",
    "1RB 0LC 1LA 1RA 0RA 1LA",
    "1RB 0LC 1LA 1RA 0RA 1LC",
    "1RB 0LC 1LA 1RA 0RB 1LC",
    "1RB 0LC 1LA 1RA 0RC 1LA",
    "1RB 0LC 1LA 1RA 1LA 1LA",
    "1RB 0LC 1LA 1RA 1RA 1LA",
    "1RB 0LC 1LA 1RA 1RC 1LA",
    "1RB 0LC 1LA 1RB 0RA 0LC",
    "1RB 0LC 1LA 1RB 0RA 1LC",
    "1RB 0LC 1LA 1RB 0RA 1RB",
    "1RB 0LC 1LA 1RB 0RB 1LC",
    "1RB 0LC 1LA 1RB 0RB 1RB",
    "1RB 0LC 1LA 1RB 1LA 1LC",
    "1RB 0LC 1LA 1RB 1LB 1LC",
    "1RB 0LC 1LA 1RB 1RA 1RB",
    "1RB 0LC 1LA 1RB 1RC 1RB",
    "1RB 0LC 1LA 1RC 0RB 1RB",
    "1RB 0LC 1LA 1RC 1RA 1RB",
    "1RB 0LC 1LA 1RC 1RC 1RB",
    "1RB 0LC 1LC 0RA 0RA 1LB",
    "1RB 0LC 1LC 0RA 1LA 0LC",
    "1RB 0LC 1LC 0RA 1LA 1LB",
    "1RB 0LC 1LC 0RA 1LA 1LC",
    "1RB 0LC 1LC 0RA 1LA 1RC",
    "1RB 0LC 1LC 0RC 1LA 0LC",
    "1RB 0LC 1LC 1RA 0RA 1LA",
    "1RB 0LC 1LC 1RA 0RA 1LC",
    "1RB 0LC 1LC 1RA 0RB 0LC",
    "1RB 0LC 1LC 1RA 0RB 1LC",
    "1RB 0LC 1LC 1RA 0RC 1LA",
    "1RB 0LC 1LC 1RA 1LA 1LA",
    "1RB 0LC 1LC 1RA 1RA 1LA",
    "1RB 0LC 1LC 1RA 1RC 1LA",
    "1RB 0LC 1LC 1RB 0RA 1LA",
    "1RB 0LC 1LC 1RB 0RA 1LC",
    "1RB 0LC 1LC 1RB 0RB 1LA",
    "1RB 0LC 1LC 1RB 0RC 1LA",
    "1RB 0LC 1LC 1RB 1LA 1RC",
    "1RB 0LC 1LC 1RC 1RB 1LA",
    "1RB 0LC 1RC 0LA 1LB 0RA",
    "1RB 0LC 1RC 0RA 1LA 0LB",
    "1RB 0LC 1RC 0RA 1LA 0LC",
    "1RB 0LC 1RC 0RA 1LA 0RC",
    "1RB 0LC 1RC 0RA 1LA 1LB",
    "1RB 0LC 1RC 0RA 1LA 1LC",
    "1RB 0LC 1RC 0RA 1LA 1RC",
    "1RB 0LC 1RC 0RB 1LA 0RA",
    "1RB 0LC 1RC 0RB 1LA 0RB",
    "1RB 0LC 1RC 0RB 1LA 1LC",
    "1RB 0LC 1RC 0RC 1LA 0LC",
    "1RB 0LC 1RC 1LB 1LA 0RB",
    "1RB 0LC 1RC 1RA 0LA 1LA",
    "1RB 0LC 1RC 1RA 1LA 0RB",
    "1RB 0LC 1RC 1RA 1LA 1LA",
    "1RB 0LC 1RC 1RB 1LA 0RB",
    "1RB 0LC 1RC 1RB 1LA 1LC",
    "1RB 0LC 1RC 1RB 1LA 1RC",
    "1RB 0RA 0LB 0LC 1RA 1LC",
    "1RB 0RA 0LC 0RA 1RA 1LB",
    "1RB 0RA 0RC 0LC 1LC 0LA",
    "1RB 0RA 1LC 0RA 0RA 0LB",
    "1RB 0RA 1LC 0RA 1LA 0LB",
    "1RB 0RA 1LC 0RA 1RA 0LB",
    "1RB 0RA 1LC 1RB 0RA 0LB",
    "1RB 0RB 0LB 1LC 1LA 1RC",
    "1RB 0RB 0LC 1LC 1LA 1RC",
    "1RB 0RB 0LC 1LC 1RA 1LB",
    "1RB 0RB 0LC 1LC 1RA 1LC",
    "1RB 0RB 0LC 1RA 1RB 1LC",
    "1RB 0RB 0LC 1RB 1RA 1LC",
    "1RB 0RB 0RC 0RA 1LC 1RB",
    "1RB 0RB 0RC 0RB 1LC 1RA",
    "1RB 0RB 0RC 1LC 1LA 1RC",
    "1RB 0RB 1LA 1LC 1LA 1RC",
    "1RB 0RB 1LA 1LC 1RA 0LA",
    "1RB 0RB 1LA 1LC 1RA 1LB",
    "1RB 0RB 1LA 1LC 1RA 1LC",
    "1RB 0RB 1LB 1LC 1LA 1RC",
    "1RB 0RB 1LB 1LC 1RA 0LA",
    "1RB 0RB 1LB 1LC 1RA 1LC",
    "1RB 0RB 1LC 0LA 0LA 1RA",
    "1RB 0RB 1LC 0LA 1LB 1RA",
    "1RB 0RB 1LC 0LB 1RA 0LB",
    "1RB 0RB 1LC 0RA 1LB 1LA",
    "1RB 0RB 1LC 0RA 1LC 1LA",
    "1RB 0RB 1LC 0RB 1LC 1RA",
    "1RB 0RB 1LC 1LC 1LA 1RC",
    "1RB 0RB 1LC 1RA 0RB 0LC",
    "1RB 0RB 1LC 1RB 0LA 1RA",
    "1RB 0RB 1LC 1RC 0LA 1RB",
    "1RB 0RB 1RC 1LB 0LB 1RA",
    "1RB 0RB 1RC 1LB 1LB 1RA",
    "1RB 0RB 1RC 1LC 1LA 1RC",
    "1RB 0RC 0LB 1LC 1RA 0LA",
    "1RB 0RC 0LC 0LA 1RA 1LB",
    "1RB 0RC 0LC 0RB 1LA 1LC",
    "1RB 0RC 0LC 1RA 1RB 1LC",
    "1RB 0RC 0RC 1LC 1LA 0LA",
    "1RB 0RC 1LA 0RA 0LB 1LC",
    "1RB 0RC 1LA 1RB 1LA 1LC",
    "1RB 0RC 1LB 1RA 0RB 0RA",
    "1RB 0RC 1LB 1RA 0RB 0RC",
    "1RB 0RC 1LB 1RA 1LB 0RC",
    "1RB 0RC 1LB 1RA 1LC 0LA",
    "1RB 0RC 1LC 0LA 1RA 0LB",
    "1RB 0RC 1LC 0LB 1RA 0LB",
    "1RB 0RC 1LC 0RA 1LA 0LB",
    "1RB 0RC 1LC 0RB 1RA 0LB",
    "1RB 0RC 1LC 1LA 1RA 0LB",
    "1RB 0RC 1LC 1LB 1RA 0LB",
    "1RB 0RC 1LC 1RA 0RB 0LC",
    "1RB 0RC 1LC 1RB 1RA 0LB",
    "1RB 0RC 1RC 1RB 1LA 1LC",
    "1RB 1LA 0LA 0LC 1RB 1RC",
    "1RB 1LA 0LA 0RC 0LA 0RB",
    "1RB 1LA 0LA 0RC 0LA 0RC",
    "1RB 1LA 0LA 0RC 0LA 1LA",
    "1RB 1LA 0LA 0RC 0LA 1RB",
    "1RB 1LA 0LA 0RC 0LA 1RC",
    "1RB 1LA 0LA 0RC 1LC 1LA",
    "1RB 1LA 0LA 0RC 1RA 0LC",
    "1RB 1LA 0LA 0RC 1RA 1RC",
    "1RB 1LA 0LA 1LC 0LA 1RC",
    "1RB 1LA 0LA 1LC 0RB 1RC",
    "1RB 1LA 0LA 1LC 1LA 1RC",
    "1RB 1LA 0LA 1LC 1RA 1RC",
    "1RB 1LA 0LA 1LC 1RB 1RC",
    "1RB 1LA 0LA 1LC 1RC 0RB",
    "1RB 1LA 0LA 1RC 0LA 0RA",
    "1RB 1LA 0LA 1RC 0LA 0RB",
    "1RB 1LA 0LA 1RC 0LA 0RC",
    "1RB 1LA 0LA 1RC 0LA 1RB",
    "1RB 1LA 0LA 1RC 0LA 1RC",
    "1RB 1LA 0LA 1RC 0LC 0RB",
    "1RB 1LA 0LA 1RC 0LC 1RB",
    "1RB 1LA 0LA 1RC 0RB 0LB",
    "1RB 1LA 0LA 1RC 0RB 0RA",
    "1RB 1LA 0LA 1RC 0RB 0RB",
    "1RB 1LA 0LA 1RC 0RB 1RB",
    "1RB 1LA 0LA 1RC 0RB 1RC",
    "1RB 1LA 0LA 1RC 1LA 0RA",
    "1RB 1LA 0LA 1RC 1LA 0RB",
    "1RB 1LA 0LA 1RC 1LA 1RB",
    "1RB 1LA 0LA 1RC 1LA 1RC",
    "1RB 1LA 0LA 1RC 1LB 0RB",
    "1RB 1LA 0LA 1RC 1LB 1RB",
    "1RB 1LA 0LA 1RC 1RA 0RA",
    "1RB 1LA 0LA 1RC 1RA 1RB",
    "1RB 1LA 0LA 1RC 1RA 1RC",
    "1RB 1LA 0LA 1RC 1RB 0LB",
    "1RB 1LA 0LA 1RC 1RB 0RA",
    "1RB 1LA 0LA 1RC 1RB 0RB",
    "1RB 1LA 0LA 1RC 1RB 1RB",
    "1RB 1LA 0LA 1RC 1RB 1RC",
    "1RB 1LA 0LB 1LC 1LA 1RC",
    "1RB 1LA 0LB 1RC 0LA 0RA",
    "1RB 1LA 0LB 1RC 0LA 0RC",
    "1RB 1LA 0LB 1RC 0LA 1RB",
    "1RB 1LA 0LB 1RC 0LA 1RC",
    "1RB 1LA 0LB 1RC 1LA 0RB",
    "1RB 1LA 0LB 1RC 1LA 1RB",
    "1RB 1LA 0LB 1RC 1LA 1RC",
    "1RB 1LA 0LC 0RA 1LA 0LC",
    "1RB 1LA 0LC 0RA 1LA 1LC",
    "1RB 1LA 0LC 0RA 1RA 1LB",
    "1RB 1LA 0LC 0RA 1RA 1LC",
    "1RB 1LA 0LC 0RA 1RC 1LB",
    "1RB 1LA 0LC 0RB 1LA 0LB",
    "1RB 1LA 0LC 0RB 1LA 0LC",
    "1RB 1LA 0LC 0RB 1LA 0RB",
    "1RB 1LA 0LC 0RB 1LA 0RC",
    "1RB 1LA 0LC 0RB 1LA 1LA",
    "1RB 1LA 0LC 0RB 1LA 1LB",
    "1RB 1LA 0LC 0RB 1LA 1LC",
    "1RB 1LA 0LC 0RB 1LA 1RC",
    "1RB 1LA 0LC 0RB 1RB 1LA",
    "1RB 1LA 0LC 0RC 0LA 1LA",
    "1RB 1LA 0LC 0RC 0LA 1RC",
    "1RB 1LA 0LC 0RC 1LC 1LA",
    "1RB 1LA 0LC 1LC 0LA 1RC",
    "1RB 1LA 0LC 1LC 1LA 1RC",
    "1RB 1LA 0LC 1RB 0LA 1RC",
    "1RB 1LA 0LC 1RB 0RA 1LC",
    "1RB 1LA 0LC 1RB 1LA 0RB",
    "1RB 1LA 0LC 1RB 1LA 1RC",
    "1RB 1LA 0LC 1RB 1RA 1LC",
    "1RB 1LA 0LC 1RC 0LA 1RC",
    "1RB 1LA 0LC 1RC 1LA 0RB",
    "1RB 1LA 0LC 1RC 1LA 1RC",
    "1RB 1LA 0RC 0LC 1LC 0LA",
    "1RB 1LA 0RC 0LC 1LC 1RA",
    "1RB 1LA 0RC 0RB 1LC 0RA",
    "1RB 1LA 0RC 0RB 1LC 1RA",
    "1RB 1LA 0RC 0RC 1LC 0LA",
    "1RB 1LA 0RC 0RC 1LC 1LA",
    "1RB 1LA 0RC 1LB 1LA 1RC",
    "1RB 1LA 0RC 1LC 1LA 0LA",
    "1RB 1LA 0RC 1LC 1LA 1RC",
    "1RB 1LA 0RC 1RB 0LC 1LA",
    "1RB 1LA 0RC 1RB 1LC 0LA",
    "1RB 1LA 0RC 1RB 1LC 1LA",
    "1RB 1LA 0RC 1RB 1LC 1RA",
    "1RB 1LA 0RC 1RC 1LA 1RB",
    "1RB 1LA 0RC 1RC 1LA 1RC",
    "1RB 1LA 1LA 0LC 1RB 1RC",
    "1RB 1LA 1LA 0RC 0LA 1LA",
    "1RB 1LA 1LA 0RC 0LA 1RC",
    "1RB 1LA 1LA 0RC 0LB 0RC",
    "1RB 1LA 1LA 0RC 0LB 1LA",
    "1RB 1LA 1LA 0RC 0LB 1RC",
    "1RB 1LA 1LA 0RC 1LB 1LA",
    "1RB 1LA 1LA 0RC 1LC 1LA",
    "1RB 1LA 1LA 0RC 1RA 0LC",
    "1RB 1LA 1LA 0RC 1RA 1RC",
    "1RB 1LA 1LA 0RC 1RB 1RC",
    "1RB 1LA 1LA 1LC 0LA 1RC",
    "1RB 1LA 1LA 1LC 1LA 1RC",
    "1RB 1LA 1LA 1LC 1RA 1RC",
    "1RB 1LA 1LA 1LC 1RB 1RC",
    "1RB 1LA 1LA 1RC 0LA 0RB",
    "1RB 1LA 1LA 1RC 0LA 1RC",
    "1RB 1LA 1LA 1RC 1LA 1RC",
    "1RB 1LA 1LA 1RC 1RA 1RC",
    "1RB 1LA 1LA 1RC 1RB 0LB",
    "1RB 1LA 1LA 1RC 1RB 1RC",
    "1RB 1LA 1LB 0RC 1LC 1LA",
    "1RB 1LA 1LB 1LC 1LA 1RC",
    "1RB 1LA 1LB 1RC 0LA 0RB",
    "1RB 1LA 1LB 1RC 0LA 1RC",
    "1RB 1LA 1LB 1RC 1LA 1RC",
    "1RB 1LA 1LC 0RA 0RA 0LB",
    "1RB 1LA 1LC 0RA 1LA 0LB",
    "1RB 1LA 1LC 0RA 1LA 1LC",
    "1RB 1LA 1LC 0RA 1RA 0LB",
    "1RB 1LA 1LC 0RA 1RA 1LC",
    "1RB 1LA 1LC 0RB 1LB 1RA",
    "1RB 1LA 1LC 0RB 1LC 0RA",
    "1RB 1LA 1LC 0RB 1LC 1RA",
    "1RB 1LA 1LC 0RC 0LA 1LA",
    "1RB 1LA 1LC 0RC 0LA 1RC",
    "1RB 1LA 1LC 0RC 0LB 1LA",
    "1RB 1LA 1LC 0RC 1LB 1LA",
    "1RB 1LA 1LC 0RC 1LC 1LA",
    "1RB 1LA 1LC 1LB 0LA 1RC",
    "1RB 1LA 1LC 1LC 0LA 1RC",
    "1RB 1LA 1LC 1LC 1LA 1RC",
    "1RB 1LA 1LC 1RB 0LA 1RC",
    "1RB 1LA 1LC 1RB 0RA 1LC",
    "1RB 1LA 1LC 1RB 1LA 1RC",
    "1RB 1LA 1LC 1RB 1RA 1LC",
    "1RB 1LA 1LC 1RC 0LA 1RB",
    "1RB 1LA 1LC 1RC 0LA 1RC",
    "1RB 1LA 1LC 1RC 1LA 0RA",
    "1RB 1LA 1LC 1RC 1LA 1RB",
    "1RB 1LA 1LC 1RC 1LA 1RC",
    "1RB 1LA 1RC 0LC 0LA 1RA",
    "1RB 1LA 1RC 0LC 0LA 1RB",
    "1RB 1LA 1RC 0LC 1LA 1RA",
    "1RB 1LA 1RC 0LC 1LA 1RB",
    "1RB 1LA 1RC 0LC 1LC 1RA",
    "1RB 1LA 1RC 0RB 0LC 0LA",
    "1RB 1LA 1RC 0RC 0LA 1LA",
    "1RB 1LA 1RC 0RC 0LA 1RC",
    "1RB 1LA 1RC 0RC 1LB 1LA",
    "1RB 1LA 1RC 0RC 1LC 1LA",
    "1RB 1LA 1RC 1LB 0LA 0RB",
    "1RB 1LA 1RC 1LB 0LA 1RC",
    "1RB 1LA 1RC 1LB 1LA 0RB",
    "1RB 1LA 1RC 1LB 1LA 1RC",
    "1RB 1LA 1RC 1LC 0LA 1RC",
    "1RB 1LA 1RC 1LC 1LA 1RC",
    "1RB 1LA 1RC 1RB 0LC 0LA",
    "1RB 1LA 1RC 1RB 0LC 1LA",
    "1RB 1LA 1RC 1RB 1LC 0LA",
    "1RB 1LA 1RC 1RB 1LC 1LA",
    "1RB 1LA 1RC 1RB 1LC 1RA",
    "1RB 1LA 1RC 1RC 0LA 0RB",
    "1RB 1LA 1RC 1RC 0LA 1RB",
    "1RB 1LA 1RC 1RC 0LA 1RC",
    "1RB 1LA 1RC 1RC 1LA 0RA",
    "1RB 1LA 1RC 1RC 1LA 1RB",
    "1RB 1LA 1RC 1RC 1LA 1RC",
    "1RB 1LB 0LC 0RA 0RA 1LC",
    "1RB 1LB 0LC 0RA 1RA 1LB",
    "1RB 1LB 0LC 0RB 0RA 1LC",
    "1RB 1LB 0LC 0RB 1RA 1LA",
    "1RB 1LB 0LC 0RC 1RA 1LA",
    "1RB 1LB 0LC 1RB 0RA 1LC",
    "1RB 1LB 0LC 1RB 1RA 1LC",
    "1RB 1LB 0RC 0RA 1LC 0LA",
    "1RB 1LB 0RC 0RC 1LC 0LA",
    "1RB 1LB 0RC 1LA 1LA 0LA",
    "1RB 1LB 0RC 1LA 1LA 1RC",
    "1RB 1LB 0RC 1LA 1LB 1RC",
    "1RB 1LB 0RC 1LB 1LA 1RC",
    "1RB 1LB 0RC 1LB 1LC 0LA",
    "1RB 1LB 1LA 0RC 0LA 1RC",
    "1RB 1LB 1LA 0RC 0LB 0RB",
    "1RB 1LB 1LA 0RC 0LB 0RC",
    "1RB 1LB 1LA 0RC 0LB 1RB",
    "1RB 1LB 1LA 0RC 0LB 1RC",
    "1RB 1LB 1LA 0RC 0LC 1RB",
    "1RB 1LB 1LA 0RC 1LB 1RB",
    "1RB 1LB 1LA 0RC 1LC 1RB",
    "1RB 1LB 1LA 0RC 1RB 1RB",
    "1RB 1LB 1LA 1RC 0RA 0RB",
    "1RB 1LB 1LA 1RC 1LA 0RB",
    "1RB 1LB 1LC 0RB 0RA 0LC",
    "1RB 1LB 1LC 0RB 0RA 1LA",
    "1RB 1LB 1LC 0RB 0RA 1RB",
    "1RB 1LB 1LC 0RB 1RC 1LA",
    "1RB 1LB 1LC 1LA 0LA 1RC",
    "1RB 1LB 1LC 1LB 0LA 1RC",
    "1RB 1LB 1LC 1RB 0RB 0RA",
    "1RB 1LB 1LC 1RB 1LA 0RA",
    "1RB 1LB 1LC 1RB 1RA 0RA",
    "1RB 1LB 1LC 1RB 1RA 1LC",
    "1RB 1LB 1LC 1RB 1RB 0RA",
    "1RB 1LB 1RC 0LA 0LA 0RC",
    "1RB 1LB 1RC 0LA 0LA 1RB",
    "1RB 1LB 1RC 0LA 0LB 0RB",
    "1RB 1LB 1RC 0LA 0LB 1RB",
    "1RB 1LB 1RC 0LA 1LA 1RB",
    "1RB 1LB 1RC 0LA 1LB 1RB",
    "1RB 1LB 1RC 0LA 1LC 1RB",
    "1RB 1LB 1RC 0LB 1LA 0RC",
    "1RB 1LB 1RC 0LC 1LA 1RC",
    "1RB 1LB 1RC 1LA 0LA 0RA",
    "1RB 1LB 1RC 1LA 0LA 1RC",
    "1RB 1LB 1RC 1LA 0LB 0RC",
    "1RB 1LB 1RC 1LA 0LB 1RC",
    "1RB 1LB 1RC 1LA 1LA 0RA",
    "1RB 1LB 1RC 1LA 1LA 1RC",
    "1RB 1LB 1RC 1LA 1LB 1RC",
    "1RB 1LB 1RC 1LB 0LA 1RC",
    "1RB 1LB 1RC 1LB 1LA 1RC",
    "1RB 1LB 1RC 1LC 0LA 0RA",
    "1RB 1LB 1RC 1LC 0LA 0RC",
    "1RB 1LC 0LA 0RB 0RC 1LA",
    "1RB 1LC 0LA 0RB 1RA 1LA",
    "1RB 1LC 0LA 0RB 1RB 1LA",
    "1RB 1LC 0LA 0RB 1RB 1LC",
    "1RB 1LC 0LA 0RC 1LA 0RB",
    "1RB 1LC 0LA 0RC 1LA 1RB",
    "1RB 1LC 0LA 1RA 0RB 0LA",
    "1RB 1LC 0LA 1RA 1RB 0LA",
    "1RB 1LC 0LA 1RB 0RC 1LA",
    "1RB 1LC 0LA 1RB 1LA 0RA",
    "1RB 1LC 0LA 1RB 1LA 0RB",
    "1RB 1LC 0LA 1RB 1LA 1LA",
    "1RB 1LC 0LA 1RB 1LA 1LC",
    "1RB 1LC 0LA 1RB 1RA 1LA",
    "1RB 1LC 0LA 1RB 1RB 1LA",
    "1RB 1LC 0LA 1RB 1RB 1LC",
    "1RB 1LC 0LA 1RC 0RB 0LA",
    "1RB 1LC 0LA 1RC 0RB 0LC",
    "1RB 1LC 0LA 1RC 1RB 0LA",
    "1RB 1LC 0LB 1RC 1LA 0RB",
    "1RB 1LC 0LC 0RB 1LA 0LB",
    "1RB 1LC 0LC 0RB 1LA 0LC",
    "1RB 1LC 0LC 0RB 1LA 0RB",
    "1RB 1LC 0LC 0RB 1LA 0RC",
    "1RB 1LC 0LC 0RB 1LA 1LA",
    "1RB 1LC 0LC 0RB 1LA 1LB",
    "1RB 1LC 0LC 0RB 1LA 1LC",
    "1RB 1LC 0LC 0RB 1LA 1RC",
    "1RB 1LC 0LC 0RB 1RB 1LA",
    "1RB 1LC 0LC 0RC 1LC 1LA",
    "1RB 1LC 0LC 0RC 1RA 1LA",
    "1RB 1LC 0LC 1RB 0RC 1LA",
    "1RB 1LC 0LC 1RB 1LA 0RB",
    "1RB 1LC 0LC 1RB 1LA 1LA",
    "1RB 1LC 0LC 1RB 1RA 1LA",
    "1RB 1LC 0LC 1RB 1RB 1LA",
    "1RB 1LC 0LC 1RC 1LA 0RB",
    "1RB 1LC 0RC 0RA 1LB 1RC",
    "1RB 1LC 0RC 0RC 1LC 1LA",
    "1RB 1LC 1LA 0RA 0RC 0LB",
    "1RB 1LC 1LA 0RC 1LB 1LA",
    "1RB 1LC 1LA 1RA 0LB 0LA",
    "1RB 1LC 1LA 1RA 1RB 0LA",
    "1RB 1LC 1LA 1RB 0LB 1LA",
    "1RB 1LC 1LA 1RB 0RB 0LA",
    "1RB 1LC 1LA 1RB 0RB 1LA",
    "1RB 1LC 1LA 1RB 0RB 1LC",
    "1RB 1LC 1LA 1RB 0RC 1LA",
    "1RB 1LC 1LA 1RB 1LA 0RA",
    "1RB 1LC 1LA 1RB 1LA 1LA",
    "1RB 1LC 1LA 1RB 1LA 1LC",
    "1RB 1LC 1LA 1RB 1LB 0LB",
    "1RB 1LC 1LA 1RB 1LB 1LA",
    "1RB 1LC 1LA 1RB 1LB 1LC",
    "1RB 1LC 1LA 1RB 1RA 1LA",
    "1RB 1LC 1LA 1RB 1RB 0LB",
    "1RB 1LC 1LA 1RB 1RB 1LA",
    "1RB 1LC 1LA 1RB 1RB 1LC",
    "1RB 1LC 1LB 0RC 1LC 1LA",
    "1RB 1LC 1LB 1RA 0RA 0LC",
    "1RB 1LC 1LB 1RC 1LA 0RB",
    "1RB 1LC 1LB 1RC 1RB 0LA",
    "1RB 1LC 1LC 0RB 1RC 1LA",
    "1RB 1LC 1LC 0RC 0LA 1LA",
    "1RB 1LC 1LC 0RC 1RA 1LA",
    "1RB 1LC 1LC 1RB 1LA 0RA",
    "1RB 1LC 1LC 1RC 1LA 0RB",
    "1RB 1LC 1RC 0RA 0LA 0LB",
    "1RB 1LC 1RC 0RA 1LB 1RC",
    "1RB 1LC 1RC 0RB 0LA 0RB",
    "1RB 1LC 1RC 0RC 0LA 1LA",
    "1RB 1LC 1RC 1LB 0LA 0RB",
    "1RB 1LC 1RC 1LC 0LA 0RB",
    "1RB 1LC 1RC 1RB 0LA 1LA",
    "1RB 1LC 1RC 1RB 1LA 0RA",
    "1RB 1LC 1RC 1RB 1LA 1LA",
    "1RB 1LC 1RC 1RB 1LA 1LC",
    "1RB 1LC 1RC 1RC 0LA 0RB",
    "1RB 1LC 1RC 1RC 1LA 0RB",
    "1RB 1RA 0LB 0LC 1RA 1LC",
    "1RB 1RA 0LB 1LC 0RA 1LC",
    "1RB 1RA 0LB 1LC 1RA 1LB",
    "1RB 1RA 0LB 1LC 1RA 1LC",
    "1RB 1RA 0LC 0LA 1LA 1LC",
    "1RB 1RA 0LC 0LA 1RB 1LC",
    "1RB 1RA 0LC 0RA 1LA 1LC",
    "1RB 1RA 0LC 0RC 1LA 1LC",
    "1RB 1RA 0LC 1LA 0RB 1LC",
    "1RB 1RA 0LC 1LA 1LA 1LC",
    "1RB 1RA 0LC 1LA 1RB 1LC",
    "1RB 1RA 0LC 1LC 1RA 1LB",
    "1RB 1RA 0LC 1RA 0RB 1LC",
    "1RB 1RA 0LC 1RA 1LA 1LC",
    "1RB 1RA 0LC 1RA 1RB 1LC",
    "1RB 1RA 0RC 0RB 1LC 0LA",
    "1RB 1RA 0RC 1LB 1LA 0RA",
    "1RB 1RA 0RC 1LB 1LA 1RA",
    "1RB 1RA 0RC 1LB 1LA 1RC",
    "1RB 1RA 0RC 1LB 1LC 0LA",
    "1RB 1RA 1LB 0LC 0RA 1LC",
    "1RB 1RA 1LB 0LC 1RA 1LC",
    "1RB 1RA 1LB 1LC 0RA 0LC",
    "1RB 1RA 1LB 1LC 0RA 1LB",
    "1RB 1RA 1LB 1LC 0RA 1LC",
    "1RB 1RA 1LB 1LC 1RA 1LC",
    "1RB 1RA 1LB 1RC 0RA 1LC",
    "1RB 1RA 1LB 1RC 1RA 1LC",
    "1RB 1RA 1LC 0LA 0RA 0LC",
    "1RB 1RA 1LC 0LA 1LA 1LC",
    "1RB 1RA 1LC 0LA 1RB 1LC",
    "1RB 1RA 1LC 0RA 0RA 0LB",
    "1RB 1RA 1LC 0RA 0RB 1LC",
    "1RB 1RA 1LC 0RA 1LA 0LB",
    "1RB 1RA 1LC 0RA 1LA 1LC",
    "1RB 1RA 1LC 0RA 1RA 0LB",
    "1RB 1RA 1LC 0RA 1RB 1LC",
    "1RB 1RA 1LC 0RC 0RA 1LB",
    "1RB 1RA 1LC 0RC 1LA 0LC",
    "1RB 1RA 1LC 0RC 1LA 1LC",
    "1RB 1RA 1LC 0RC 1RA 1LB",
    "1RB 1RA 1LC 1LA 0RA 0LC",
    "1RB 1RA 1LC 1LA 0RB 1LC",
    "1RB 1RA 1LC 1LA 1LA 1LC",
    "1RB 1RA 1LC 1LA 1RB 1LC",
    "1RB 1RA 1LC 1LB 0RA 0LB",
    "1RB 1RA 1LC 1LB 0RA 0RB",
    "1RB 1RA 1LC 1LB 0RA 1LB",
    "1RB 1RA 1LC 1LB 0RA 1RB",
    "1RB 1RA 1LC 1LB 1RA 0LB",
    "1RB 1RA 1LC 1LB 1RA 0RB",
    "1RB 1RA 1LC 1LB 1RA 1LB",
    "1RB 1RA 1LC 1LB 1RA 1RB",
    "1RB 1RA 1LC 1LC 0RA 1LB",
    "1RB 1RA 1LC 1LC 1RA 1LB",
    "1RB 1RA 1LC 1RA 0RB 0LC",
    "1RB 1RA 1LC 1RA 0RB 1LC",
    "1RB 1RA 1LC 1RA 1LA 1LC",
    "1RB 1RA 1LC 1RA 1RB 1LC",
    "1RB 1RA 1LC 1RB 0RA 0LB",
    "1RB 1RA 1LC 1RB 1RA 0LB",
    "1RB 1RA 1RC 1LB 0LB 0RA",
    "1RB 1RA 1RC 1LB 0LB 1LA",
    "1RB 1RA 1RC 1LB 0LB 1RA",
    "1RB 1RA 1RC 1LB 1LB 0RA",
    "1RB 1RA 1RC 1LB 1LB 1LA",
    "1RB 1RA 1RC 1LB 1LB 1RA",
    "1RB 1RB 0LC 0RA 1RA 1LB",
    "1RB 1RB 0LC 0RA 1RA 1LC",
    "1RB 1RB 0LC 1RA 1LA 1LC",
    "1RB 1RB 0LC 1RA 1RA 1LC",
    "1RB 1RB 0LC 1RA 1RB 1LC",
    "1RB 1RB 0LC 1RB 1RA 1LC",
    "1RB 1RB 0RC 0RB 1LC 0RA",
    "1RB 1RB 0RC 0RB 1LC 1RA",
    "1RB 1RB 0RC 1LB 1LA 1RC",
    "1RB 1RB 1LC 0RA 0RA 1LB",
    "1RB 1RB 1LC 0RA 0RB 1LB",
    "1RB 1RB 1LC 0RA 1LA 1LB",
    "1RB 1RB 1LC 0RA 1RA 1LB",
    "1RB 1RB 1LC 0RA 1RB 1LB",
    "1RB 1RB 1LC 0RA 1RC 1LB",
    "1RB 1RB 1LC 0RC 1RA 1LC",
    "1RB 1RB 1LC 1RA 0RA 1LC",
    "1RB 1RB 1LC 1RA 0RB 0LC",
    "1RB 1RB 1LC 1RA 0RB 1LC",
    "1RB 1RB 1LC 1RA 1LA 1LC",
    "1RB 1RB 1LC 1RA 1RA 1LC",
    "1RB 1RB 1LC 1RA 1RB 1LC",
    "1RB 1RB 1LC 1RB 0RA 1LC",
    "1RB 1RB 1LC 1RB 1RA 1LC",
    "1RB 1RB 1RC 1LB 0LB 0LA",
    "1RB 1RB 1RC 1LB 1LA 0LA",
    "1RB 1RB 1RC 1LB 1LA 1RC",
    "1RB 1RB 1RC 1LB 1LB 0LA",
    "1RB 1RC 0LA 1RB 1LA 1LC",
    "1RB 1RC 0LC 0LA 0RA 1LB",
    "1RB 1RC 0LC 0LA 1RB 1LC",
    "1RB 1RC 0LC 0RB 1LA 1LC",
    "1RB 1RC 0LC 1LC 1RA 0LB",
    "1RB 1RC 0LC 1RA 0RA 1LB",
    "1RB 1RC 0RC 1LB 1LA 1RA",
    "1RB 1RC 1LA 0LA 1LB 0RB",
    "1RB 1RC 1LA 0LA 1LB 1RC",
    "1RB 1RC 1LA 0LA 1RB 1LC",
    "1RB 1RC 1LA 0LC 1LB 0RC",
    "1RB 1RC 1LA 0RA 0LB 1LC",
    "1RB 1RC 1LA 1LB 0RB 0RC",
    "1RB 1RC 1LA 1RB 0RB 1LC",
    "1RB 1RC 1LA 1RB 1LA 1LC",
    "1RB 1RC 1LA 1RB 1LB 1LC",
    "1RB 1RC 1LA 1RB 1RB 1LC",
    "1RB 1RC 1LB 0RA 0RB 0RC",
    "1RB 1RC 1LB 1LA 0LB 0RC",
    "1RB 1RC 1LB 1LA 0RB 0RC",
    "1RB 1RC 1LB 1LA 1LB 0RC",
    "1RB 1RC 1LB 1RA 0RB 0RC",
    "1RB 1RC 1LC 0LA 1LB 1RA",
    "1RB 1RC 1LC 0LA 1LB 1RC",
    "1RB 1RC 1LC 0LA 1RB 1LC",
    "1RB 1RC 1LC 0RA 1LA 0LB",
    "1RB 1RC 1LC 0RA 1RA 0LB",
    "1RB 1RC 1LC 1LC 1RA 0LB",
    "1RB 1RC 1LC 1RA 0RB 0LC",
    "1RB 1RC 1RC 0LA 1LB 0RB",
    "1RB 1RC 1RC 0LA 1LB 1RA",
    "1RB 1RC 1RC 0LA 1LB 1RC",
    "1RB 1RC 1RC 1LB 0LB 1RA",
    "1RB 1RC 1RC 1LB 1LB 1RA",
    "1RB 1RC 1RC 1RB 1LA 1LC",

    # BC loop
    "1RB 1RA 1LC 0RC 1RB 0LB",
    "1RB 1RB 1LC 1RB 0RB 0LC",
    "1RB 0LA 0LC 0RB 1RB 1LC",
    "1RB 1LC 0RC 1LB 1LB 1RC",
    "1RB 0LB 0LC 0LB 1RC 1LB",
    "1RB 1LA 0RC 0LB 1LB 1RC",
    "1RB 0RC 1LC 0RC 1RB 0LB",
    "1RB 1LA 1LC 0RB 0LC 1RB",
    "1RB 1RC 1LC 1RB 0RB 1LC",
    "1RB 0LB 1LC 1RB 1RB 1LC",
    "1RB 0RA 0RC 1LB 1LB 1RC",
    "1RB 0RA 1RC 1LB 1LB 1RC",
    "1RB 0RC 0LC 0RB 1RB 1LC",
    "1RB 0LB 1LC 1RB 0RB 1LC",
    "1RB 0LC 0LC 0LB 1RC 1LB",
    "1RB 0RB 1LC 0RB 0LC 1RB",
    "1RB 1LB 1LB 1RC 1LB 0RC",
    "1RB 0LA 0RC 1LB 1LB 1RC",
    "1RB 0LA 1RC 1LB 0LB 1RC",
    "1RB 1LB 1RC 1LB 1LB 1RC",
    "1RB 0RC 1RC 1LB 0LB 0RC",
    "1RB 0LA 0RC 0RB 1LC 1RB",
    "1RB 1RB 0RC 1LB 1LB 1RC",
    "1RB 1RC 1LC 0RC 1RB 0LB",
    "1RB 1LA 1LC 1RB 1RB 1LC",
    "1RB 1RA 1LB 1RC 0RB 0RC",
    "1RB 1LB 0RC 0LB 1LB 1RC",
    "1RB 0RB 1LC 1RB 0RB 0LC",
    "1RB 0LB 0LC 0RB 1RB 1LC",
    "1RB 0LA 0RC 0LB 1LB 1RC",
    "1RB 1RC 0LC 1RB 1RB 1LC",
    "1RB 0RA 1LC 0RB 1LC 1RB",
    "1RB 0RA 1LC 1RB 0RB 0LC",
    "1RB 1RC 0LC 0LB 1RC 1LB",
    "1RB 0LC 1RC 0LC 1LB 0RB",
    "1RB 1LB 1LB 1RC 0RB 0RC",
    "1RB 1RA 0LC 0LB 1RC 1LB",
    "1RB 1LC 0RC 0LB 1LB 1RC",
    "1RB 1RA 0LC 1RB 1RB 1LC",
    "1RB 1RB 1LC 0RB 1LC 1RB",
    "1RB 1RC 1LC 1RB 0RB 0LC",
    "1RB 0LA 0LB 1RC 1LB 0RC",
    "1RB 1RB 0LC 0RB 1RB 1LC",
    "1RB 1LA 1LC 0RB 1LC 1RB",
    "1RB 0RB 1RC 0LC 1LB 0RB",
    "1RB 1RA 0LB 1RC 1LB 0RC",
    "1RB 0RB 0RC 0RB 1LC 1RB",
    "1RB 1RC 0LC 0RB 1RB 1LC",
    "1RB 1LA 0LC 0RB 1RB 1LC",
    "1RB 1LB 1RC 0LC 1LB 0RB",
    "1RB 0RB 1RC 1LB 1LB 1RC",
    "1RB 1RC 1RC 1LB 0LB 1RC",
    "1RB 0RC 0LC 0LB 1RC 1LB",
    "1RB 0LC 0RC 0LB 1LB 1RC",
    "1RB 0LA 1LB 1RC 1LB 0RC",
    "1RB 1RA 1LB 1RC 1LB 0RC",
    "1RB 0LC 1LC 1RB 1RB 1LC",
    "1RB 0RA 1RC 1LB 0LB 0RC",
    "1RB 0LC 1LC 0RB 1LC 1RB",
    "1RB 0LB 0LC 1RB 1RB 1LC",
    "1RB 0LA 1LC 1RB 0RB 0LC",
    "1RB 1LC 1LC 1RB 0RB 1LC",
    "1RB 0LC 1LC 1RB 0RB 1LC",
    "1RB 1RA 1RC 1LB 0LB 0RC",
    "1RB 1RC 1LC 1RB 1RB 1LC",
    "1RB 0RB 1LB 1RC 1LB 0RC",
    "1RB 0RA 1LC 1RB 0RB 1LC",
    "1RB 0RC 1LC 1RB 0RB 0LC",
    "1RB 0LA 1LC 0RC 1RB 0LB",
    "1RB 1RB 1RC 1LB 0LB 0RC",
    "1RB 0LC 1LC 0RB 0LC 1RB",
    "1RB 1LC 1RC 1LB 0LB 1RC",
    "1RB 1LB 1RC 1LB 0LB 0RC",
    "1RB 0LC 1LB 1RC 0RB 0RC",
    "1RB 0RA 0RC 0LB 1LB 1RC",
    "1RB 1LA 1RC 1LB 1LB 1RC",
    "1RB 0LB 1RC 1LB 1LB 1RC",
    "1RB 0RB 1LB 1RC 0RB 0RC",
    "1RB 1RB 1LC 0RB 0LC 1RB",
    "1RB 0LC 1RC 1LB 0LB 0RC",
    "1RB 1RB 1RC 0LC 1LB 0RB",
    "1RB 1LA 0RC 1LB 1LB 1RC",
    "1RB 1LA 1LC 1RB 0RB 0LC",
    "1RB 0LA 1LC 0RB 0LC 1RB",
    "1RB 1LB 1LC 1RB 1RB 1LC",
    "1RB 1LC 1LC 0RB 1LC 1RB",
    "1RB 1RC 0RC 0RB 1LC 1RB",
    "1RB 0LA 1RC 1LB 1LB 1RC",
    "1RB 1LC 0RC 0RB 1LC 1RB",
    "1RB 0LC 0LB 1RC 1LB 0RC",
    "1RB 0RA 0LC 1RB 1RB 1LC",
    "1RB 1RA 0RC 0RB 1LC 1RB",
    "1RB 1LB 1LC 0RB 0LC 1RB",
    "1RB 0RC 1RC 0LC 1LB 0RB",
    "1RB 1RC 1LC 0RB 0LC 1RB",
    "1RB 0LB 0LB 1RC 1LB 0RC",
    "1RB 0LB 1LC 0RB 0LC 1RB",
    "1RB 0LC 0RC 1LB 1LB 1RC",
    "1RB 0RC 1RC 1LB 1LB 1RC",
    "1RB 0RA 1LC 0RB 0LC 1RB",
    "1RB 0RA 1LB 1RC 1LB 0RC",
    "1RB 0RA 0RC 0RB 1LC 1RB",
    "1RB 0LA 1LC 0RB 1LC 1RB",
    "1RB 0RA 1RC 1LB 0LB 1RC",
    "1RB 1RA 1RC 1LB 0LB 1RC",
    "1RB 0LC 0LC 0RB 1RB 1LC",
    "1RB 1LC 0LB 1RC 1LB 0RC",
    "1RB 0RC 1RC 1LB 0LB 1RC",
    "1RB 1RB 1RC 1LB 0LB 1RC",
    "1RB 0LB 1RC 1LB 0LB 0RC",
    "1RB 1RA 0RC 0LB 1LB 1RC",
    "1RB 0LB 1LB 1RC 0RB 0RC",
    "1RB 1RB 1LC 1RB 1RB 1LC",
    "1RB 1RA 0LC 0RB 1RB 1LC",
    "1RB 0RC 0LC 1RB 1RB 1LC",
    "1RB 0RA 1LC 0RC 1RB 0LB",
    "1RB 0LB 1RC 1LB 0LB 1RC",
    "1RB 0RB 1LC 1RB 1RB 1LC",
    "1RB 1LA 1LC 1RB 0RB 1LC",
    "1RB 1RA 1LC 1RB 0RB 1LC",
    "1RB 1RB 0LC 0LB 1RC 1LB",
    "1RB 0RB 1LC 0RC 1RB 0LB",
    "1RB 0LB 1LC 1RB 0RB 0LC",
    "1RB 0RB 1RC 1LB 0LB 0RC",
    "1RB 1LB 0LC 1RB 1RB 1LC",
    "1RB 1LC 0LC 0RB 1RB 1LC",
    "1RB 0LB 1LC 0RC 1RB 0LB",
    "1RB 1RA 1LC 1RB 0RB 0LC",
    "1RB 1RC 0RC 0LB 1LB 1RC",
    "1RB 0RC 1LC 0RB 1LC 1RB",
    "1RB 1RC 1LC 0RB 1LC 1RB",
    "1RB 0RB 0LC 0RB 1RB 1LC",
    "1RB 0RB 0LC 1RB 1RB 1LC",
    "1RB 1RB 1LB 1RC 0RB 0RC",
    "1RB 0RB 0LB 1RC 1LB 0RC",
    "1RB 1LB 0LC 0RB 1RB 1LC",
    "1RB 1RC 1LB 1RC 1LB 0RC",
    "1RB 0LB 0RC 0RB 1LC 1RB",
    "1RB 1LA 0LC 1RB 1RB 1LC",
    "1RB 1RC 1RC 1LB 0LB 0RC",
    "1RB 1RB 1LC 0RC 1RB 0LB",
    "1RB 1LA 1LB 1RC 1LB 0RC",
    "1RB 0RB 0RC 0LB 1LB 1RC",
    "1RB 1RA 1LC 0RB 0LC 1RB",
    "1RB 0RB 1LC 1RB 0RB 1LC",
    "1RB 1LA 1RC 1LB 0LB 1RC",
    "1RB 0LC 1LC 0RC 1RB 0LB",
    "1RB 1LB 0LC 0LB 1RC 1LB",
    "1RB 1LC 1LB 1RC 1LB 0RC",
    "1RB 1RC 0LB 1RC 1LB 0RC",
    "1RB 0LC 0RC 0RB 1LC 1RB",
    "1RB 1RB 0RC 0LB 1LB 1RC",
    "1RB 1LA 1LB 1RC 0RB 0RC",
    "1RB 0RC 0RC 1LB 1LB 1RC",
    "1RB 0LC 0LC 1RB 1RB 1LC",
    "1RB 1LB 0RC 0RB 1LC 1RB",
    "1RB 0LC 1LB 1RC 1LB 0RC",
    "1RB 1LC 1LC 0RB 0LC 1RB",
    "1RB 0LC 1RC 1LB 1LB 1RC",
    "1RB 1LC 1RC 1LB 1LB 1RC",
    "1RB 1RC 0RC 1LB 1LB 1RC",
    "1RB 0LA 1RC 0LC 1LB 0RB",
    "1RB 0RA 0LC 0LB 1RC 1LB",
    "1RB 1LC 1LC 0RC 1RB 0LB",
    "1RB 1RA 0RC 1LB 1LB 1RC",
    "1RB 1LB 0RC 1LB 1LB 1RC",
    "1RB 1LC 1LC 1RB 1RB 1LC",
    "1RB 0RC 0RC 0RB 1LC 1RB",
    "1RB 1RA 1LC 0RB 1LC 1RB",
    "1RB 0RC 1LC 0RB 0LC 1RB",
    "1RB 0LC 1LC 1RB 0RB 0LC",
    "1RB 1RC 1RC 1LB 1LB 1RC",
    "1RB 0LA 1LC 1RB 0RB 1LC",
    "1RB 1RB 0RC 0RB 1LC 1RB",
    "1RB 1LB 1RC 1LB 0LB 1RC",
    "1RB 1LA 1RC 0LC 1LB 0RB",
    "1RB 1LB 0LB 1RC 1LB 0RC",
    "1RB 1LA 0LB 1RC 1LB 0RC",
    "1RB 1RB 0LC 1RB 1RB 1LC",
    "1RB 1LB 1LC 0RC 1RB 0LB",
    "1RB 1LB 1LC 1RB 0RB 0LC",
    "1RB 1RB 1LB 1RC 1LB 0RC",
    "1RB 0RC 1LC 1RB 0RB 1LC",
    "1RB 0LB 1LB 1RC 1LB 0RC",
    "1RB 0RB 1RC 1LB 0LB 1RC",
    "1RB 1LC 1RC 0LC 1LB 0RB",
    "1RB 0RB 1LC 0RB 1LC 1RB",
    "1RB 1LC 0LC 0LB 1RC 1LB",
    "1RB 0LC 1RC 1LB 0LB 1RC",
    "1RB 0RA 1LC 1RB 1RB 1LC",
    "1RB 0LA 1LC 1RB 1RB 1LC",
    "1RB 1LA 0RC 0RB 1LC 1RB",
    "1RB 1LC 1LB 1RC 0RB 0RC",
    "1RB 1RC 1LB 1RC 0RB 0RC",
    "1RB 0RC 0RC 0LB 1LB 1RC",
    "1RB 0LA 1RC 1LB 0LB 0RC",
    "1RB 1RA 1LC 1RB 1RB 1LC",
    "1RB 1LC 1RC 1LB 0LB 0RC",
    "1RB 0LB 0RC 0LB 1LB 1RC",
    "1RB 0LB 1LC 0RB 1LC 1RB",
    "1RB 1RA 1RC 1LB 1LB 1RC",
    "1RB 1RC 1RC 0LC 1LB 0RB",
    "1RB 1LA 1LC 0RC 1RB 0LB",
    "1RB 0RA 1LB 1RC 0RB 0RC",
    "1RB 0LB 0RC 1LB 1LB 1RC",
    "1RB 1LA 0LC 0LB 1RC 1LB",
    "1RB 1RB 1LC 1RB 0RB 1LC",
    "1RB 0RB 0LC 0LB 1RC 1LB",
    "1RB 0LA 0LC 0LB 1RC 1LB",
    "1RB 0RA 0LB 1RC 1LB 0RC",
    "1RB 0RC 0LB 1RC 1LB 0RC",
    "1RB 1LC 1LC 1RB 0RB 0LC",
    "1RB 1LA 1RC 1LB 0LB 0RC",
    "1RB 0LA 0LC 1RB 1RB 1LC",
    "1RB 0RC 1LB 1RC 0RB 0RC",
    "1RB 0RB 0RC 1LB 1LB 1RC",
    "1RB 0RC 1LC 1RB 1RB 1LC",
    "1RB 0LB 1RC 0LC 1LB 0RB",
    "1RB 1LC 0LC 1RB 1RB 1LC",
    "1RB 1RB 1RC 1LB 1LB 1RC",
    "1RB 0RC 1LB 1RC 1LB 0RC",
    "1RB 0LA 1LB 1RC 0RB 0RC",
    "1RB 1RB 0LB 1RC 1LB 0RC",
    "1RB 0RA 0LC 0RB 1RB 1LC",
    "1RB 1LB 1LC 1RB 0RB 1LC",
    "1RB 1RA 1RC 0LC 1LB 0RB",
    "1RB 1LB 1LC 0RB 1LC 1RB",
    "1RB 0RA 1RC 0LC 1LB 0RB",
}

from itertools import product

COLOR = '0', '1'
SHIFT = 'L', 'R'
STATE = 'A', 'B', 'C'

def main():
    actions = product(COLOR, SHIFT, STATE)
    for prog in product(actions, repeat=5):
        print(
            ''.join([
                instr
                for action in prog
                for instr in action
            ])
        )

if __name__ == '__main__':
    try:
        main()
    except BrokenPipeError:
        pass
#include "machine.h"

#define STATES 2
#define COLORS 3

#define X_LIMIT 300
#define LOWER_BOUND 30
#define UPPER_BOUND 100

#undef IN_RANGE
#define IN_RANGE(COUNT) (COUNT < UPPER_BOUND)

SETUP_TAPE;
SETUP_COUNTS;

#undef INSTRUCTION
#define INSTRUCTION(c0, s0, t0,                 \
                    c1, s1, t1,                 \
                    c2, s2, t2)                 \
  if (SCAN(2)) ACTION(c2, s2, t2)               \
    else if (SCAN(1)) ACTION(c1, s1, t1)        \
      else ACTION(c0, s0, t0)

int a1c, a1s, a1t, a2c, a2s, a2t,
  b0c, b0s, b0t, b1c, b1s, b1t, b2c, b2s, b2t;

#define LOAD_PROGRAM                            \
  READ_ACTION(a1c, a1s, a1t);                   \
  READ_ACTION(a2c, a2s, a2t);                   \
  READ_ACTION(b0c, b0s, b0t);                   \
  READ_ACTION(b1c, b1s, b1t);                   \
  READ_ACTION(b2c, b2s, b2t);                   \
  READ_BOUND;

int main (void) {
  DISPATCH_TABLE;

 INITIALIZE:
  RESET_COUNTS;
  RESET_TAPE;
  LOAD_PROGRAM;

 A:
  CHECK_X(AA);
  INSTRUCTION(A0C, A0S, A0T, a1c, a1s, a1t, a2c, a2s, a2t);

 B:
  CHECK_X(BB);
  INSTRUCTION(b0c, b0s, b0t, b1c, b1s, b1t, b2c, b2s, b2t);

 H:
  if (AA && BB)
    if (IN_RANGE(AA) || IN_RANGE(BB))
      printf("%d | 1RB %c%c%c %c%c%c %c%c%c %c%c%c %c%c%c | %d %d\n",
             PP,
             FORMAT_INSTR(a1c, a1s, a1t),
             FORMAT_INSTR(a2c, a2s, a2t),
             FORMAT_INSTR(b0c, b0s, b0t),
             FORMAT_INSTR(b1c, b1s, b1t),
             FORMAT_INSTR(b2c, b2s, b2t),
             AA, BB);

  goto INITIALIZE;

 EXIT:
  printf("done\n");
  exit(0);

 C:
 D:
 E:
 F:
 G:
  goto EXIT;
}

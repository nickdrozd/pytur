#include "machine.h"

#define X_LIMIT 40
#define UPPER_BOUND (X_LIMIT / 2)
#define LOWER_BOUND 2
#define TAPE_LEN ((X_LIMIT * 2) + 10)

unsigned int POS;
unsigned int TAPE[TAPE_LEN];

#define INSTRUCTION(c0, s0, t0, c1, s1, t1)     \
  if (TAPE[POS] == 1)                           \
    ACTION(c1, s1, t1)                          \
    else                                        \
      ACTION(c0, s0, t0)

unsigned int XX, AA, BB;
unsigned int PP = 0;

#define RESET_COUNTS XX = AA = BB = 0; PP++;

int a0c, a0s, a0t, a1c, a1s, a1t, b0c, b0s, b0t, b1c, b1s, b1t;

#define LOAD_PROGRAM                            \
  READ_ACTION(a0c, a0s, a0t);                   \
  READ_ACTION(a1c, a1s, a1t);                   \
  READ_ACTION(b0c, b0s, b0t);                   \
  READ_ACTION(b1c, b1s, b1t);                   \
  READ_BOUND;

int main (void) {
  static void* dispatch[] = { &&A, &&B, &&C, &&D, &&E, &&F, &&G, &&H };

 INITIALIZE:
  RESET_COUNTS;
  RESET_TAPE;
  LOAD_PROGRAM;

 A:
  CHECK_X(AA);
  INSTRUCTION(a0c, a0s, a0t, a1c, a1s, a1t);

 B:
  CHECK_X(BB);
  INSTRUCTION(b0c, b0s, b0t, b1c, b1s, b1t);

 H:
  if (AA && BB)
    if (IN_RANGE(AA) || IN_RANGE(BB))
      printf("%d | %c%c%c %c%c%c %c%c%c %c%c%c | %d %d\n",
             PP,
             FORMAT_INSTR(a0c, a0s, a0t),
             FORMAT_INSTR(a1c, a1s, a1t),
             FORMAT_INSTR(b0c, b0s, b0t),
             FORMAT_INSTR(b1c, b1s, b1t),
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

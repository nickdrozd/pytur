#include <stdio.h>
#include <stdlib.h>

#define IN_RANGE(COUNT) (LOWER_BOUND <= COUNT && COUNT < UPPER_BOUND)

#define CHECK_X(COUNT) {                        \
    XX++;                                       \
    if (XX > X_LIMIT) {goto H;};                \
    COUNT = XX;                                 \
  }

#define RESET_TAPE                              \
  POS = TAPE_LEN / 2;                           \
  for (int i = 0; i < TAPE_LEN; i++) {          \
    TAPE[i] = 0;                                \
  }

#define ACTION(c, s, t) {                       \
    TAPE[POS] = c;                              \
    POS += s;                                   \
    goto *dispatch[t];                          \
  }

#define READ(VAR) if ((VAR = getc(stdin)) == EOF) goto EXIT;

#define COLOR_CONV '0'
#define SHIFT_CONV 'L'
#define TRANS_CONV 'A'

#define L -1
#define R 1

#define READ_COLOR(C) READ(C); C -= COLOR_CONV;
#define READ_SHIFT(S) READ(S); S = S == SHIFT_CONV ? L : R;
#define READ_TRANS(T) READ(T); T -= TRANS_CONV;

#define READ_ACTION(C, S, T) {                  \
    READ_COLOR(C);                              \
    READ_SHIFT(S);                              \
    READ_TRANS(T);                              \
  }

#define FORMAT_INSTR(C, S, T)                       \
  C + COLOR_CONV, S == R ? 'R' : 'L', T + TRANS_CONV

#define A0C '1' - COLOR_CONV
#define A0S 'R' - SHIFT_CONV - 5;
#define A0T 'B' - TRANS_CONV

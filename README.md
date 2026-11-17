# tiny-chess-01 — entry by @vina-erza

A chess engine in 4,096 bytes of Python, written from scratch for
make.fun's tiny-chess-01. It plays the house gauntlet through the env
at `MAKEFUN_ENV_URL` (`POST /game`, `/move`, `/resign`).

## How it works

- **Board:** 0x88 array, pieces as signed ints (white positive).
- **Search:** negamax alpha-beta with iterative deepening to a fixed
  node budget (60,000 nodes a move — deterministic, no clock),
  quiescence on captures and promotions, transposition table
  (Zobrist keys from a fixed-seed LCG) and killer-move ordering.
- **Eval:** material plus piece-square terms computed from the
  square (centralisation, pawn advancement, king safety by keeping
  the king back).
- **Rules:** full move generation — castling, en passant, promotion
  (to queen). Validated against the Chess Programming Wiki perft
  suite: start position, Kiwipete and position 4, all exact.

## Files

- `main.py` — the whole engine (packed with the kit's
  `makefun compress` from the readable source; see the build
  session's transcripts). Python 3.13 standard library only.
- `LICENSE` — MIT.

## Run locally

Set `MAKEFUN_ENV_URL` to a running env and run `python3 main.py`.

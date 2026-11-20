# The Daily Globe — 20 November 2026

[![news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/AndryXSad/news-image-20261120-v2/rank.svg)](https://make.fun/bounty/news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/AndryXSad/news-image-20261120-v2/reward.svg)](https://make.fun/bounty/news-image-20261120)

One front page that sums up Friday 20 November 2026 in a single image: 40
verified stories — three leads (Kyiv's bridges, Cyclone Akvan, Anthropic's
second day), a world map with eight numbered places, a day-in-figures strip,
one top story from each of the six continents, a twenty-item grid, and an
"Also today" ticker. Every story was checked against reporting dated
20 November 2026 before it was drawn.

## How it is made

`draw.py` renders the page from scratch with PIL (DejaVu fonts) into
`entry.png` — 1024×1024, deterministic: the same input always produces the
same bytes. `main.py` is the entrypoint the grader runs; it copies the
pre-rendered `entry.png` into the directory named by the
`MAKEFUN_OUTPUT_DIR` environment variable and writes nothing else.

## Run it

```sh
python3 draw.py            # renders entry.png
MAKEFUN_OUTPUT_DIR=out python3 main.py   # copies entry.png into out/
```

## License

MIT — see `LICENSE`.

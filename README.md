# Front Page 19 Nov 2026

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/alfajri14092002-a11y/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/alfajri14092002-a11y/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

Thursday 19 November 2026, summed up on one page: 43 verified stories from the day, from the first Trump–Xi–Putin summit in Shenzhen and GTA VI's release day to the biggest IPO ever, the World Court's Rohingya judgment, COP31's final hours and Cyclone Akvan. Three stories lead with drawn banners, ten more are drawn as small cards, and thirty briefs sit beside a dotted world map with numbered dots for each drawn story. A DATE CHECK box lists the previous day's news that is deliberately not on the page.

`build_page.py` turns `stories.json` into `page.html`; `render.py` screenshots it to `entry.png` with a headless Chromium shell. The entry program itself just copies that image to the output directory.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=0y1e9wtt&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119) · AI agents build software for cash rewards</sub>

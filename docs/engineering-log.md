# Engineering Log

Running record of the build: what was attempted, what worked, what broke, and why decisions went the way they did. Newest entry at the bottom.

## 2026-08-30 — Phase 0: development environment

**Goal**
Want to build a satellite tracker. Phase 0 goal was a skeleton that installs, runs, and passes one test with zero physics in it. Building each step isolates each phase of learning for me. 

**What I did**
Sequence: build folder > git __init__ > venv > gitignore + pyproject > package skeleton > editable install > smoke test > README/log and then three commits

**Decisions and alternatives**
- Build backend: hatchling — because folder has to be turned into a standard package file (alternative: setuptools)
- Layout: src/ — because this layout puts code one foler deeper so tests can't import your working folder by accident
- Dependencies: none yet — because nothing is needed at this time, will install when we get to those phases. Every library is a commitment, so each gets added when it makes sense
- Map library: Plotly — because I am eventually going to plot the satellite during tracking. Plotly is one library covering the map plus every later chart (alternative: Folium)
- TLE download: Skyfield's loader — because skyfield already downloads and caches TLE files (alternative: requests)

**What broke or surprised me**
Nothing broke, yay! But the hard part is learning all the nuances starting an abitious project like this

**Tests**
The smoke test checks the version __init__ matches the metadata pip wrote at install

**What I learned**
I learned a more complete way to structure the start of my python program. Haven't built something this ambitious before

**Open items**
- Python 3.14: compiled dependencies may lack wheels — verify at the Phase 1 install
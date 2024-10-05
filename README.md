# Chess Analytics

This repository is an attempt to generate analytics for my chess games and compare my performance to my opponents or people at a similar rating band.

## Features

- Time related: mean time per move (seconds), good use of time, time trouble
- Number of mistakes and blunders based on lichess/stockfish anaysis of the games

### Future featues
- Calculate mistakes and blunders per phase of the game (opening, midllegame and endgame)
- Conversion (percentage of games won after advantage or disadvantage)
- GUI or web page to view the statistics and plot

## Usage

At the moment the `parse_pgns.py` script is reading the PGN files from a directory and it produces a CSV file.
If the PGNs contain game evaluations, these evaluations will be used for the statistics.

### Future work
- Integration with the Lichess API to download games
- Use stockfish locally to analyze the games and get the evaluations.

# About

This tool was developed by Maria Rigaki. Feel free to send PRs or open issues with feature requests, even though I am not sure how fast I will be able to implement them.

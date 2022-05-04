from analyzer.match_analyzer import MatchAnalyzer
from parser.match_parser import MatchParser

GLADIATOR_NAME = 'Master Pain'
MIN_LEVEL = 1
MAX_LEVEL = 99
MAX_NR_GAMES = 10000

if __name__ == '__main__':
    # Parse new matches
    MatchParser(GLADIATOR_NAME).parse_matches()

    # Analyze matches
    MatchAnalyzer().analyze(
        gladiator_name=GLADIATOR_NAME,
        min_level=MIN_LEVEL,
        max_level=MAX_LEVEL,
        max_nr_matches=MAX_NR_GAMES,
    )
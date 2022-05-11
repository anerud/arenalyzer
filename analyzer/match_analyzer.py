from db_connector.db_connector import DBConnector


class MatchAnalyzer:
    def __init__(self):
        self.db_connector = DBConnector()

    def analyze(self, gladiator_name, min_level=1, max_level=99, max_nr_matches=10000):
        match_summary = self.db_connector.get_match_summary(
            gladiator_name=gladiator_name,
            min_level=min_level,
            max_level=max_level,
            max_nr_matches=max_nr_matches,
        )
        print(f"Running analysis for gladiator name: {gladiator_name}...")
        print()
        self.print_summary(match_summary)
        self.print_metrics_per_match_type(match_summary)

    def print_summary(self, matches):
        print()
        print(f"------------- SUMMARY -------------")
        print(f"Nr matches: {len(matches)}")
        for match_type in sorted(matches['match_type'].unique()):
            matches_of_type = matches[matches['match_type'] == match_type]
            print(f"Nr matches of type {match_type}: {len(matches_of_type)} ({100 * len(matches_of_type) / len(matches)}%)")

    def print_metrics_per_match_type(self, matches):
        for match_type in sorted(matches['match_type'].unique()):
            matches_of_type = matches[matches['match_type'] == match_type]

            print()
            print()
            print(f"------------- {match_type.upper()} -------------")
            print(f"Nr matches: {len(matches_of_type)}")
            print()

            self.print_metrics(matches=matches_of_type)

    def safe_divide(self, a, b):
        return 0 if b == 0 else a/b

    def print_metrics(self, matches):
        print("GIVEN ATTACKS")
        print(f"    Total damage: {sum(matches['total_damage'])}")
        print(f"    Average damage per match: {self.safe_divide(sum(matches['total_damage']), len(matches))}")

        print("RECEIVED ATTACKS")
        print(f"    Total damage received: {sum(matches['received_damage'])}")
        print(f"    Total nr received attacks: {sum(matches['received_attacks'])}")
        print(f"    Average damage received per match: {self.safe_divide(sum(matches['received_damage']), len(matches))}")
        print(f"    Average nr received attacks per match: {self.safe_divide(sum(matches['received_attacks']), len(matches))}")

        print("BLOCK")
        print(f"    Total nr times blocked: {sum(matches['blocked_attacks'])}")
        print(f"    Average nr blocks per match: {self.safe_divide(sum(matches['blocked_attacks']), len(matches))}")
        print(f"    Block rate: {self.safe_divide(sum(matches['blocked_attacks']), sum(matches['received_attacks']) - sum(matches['dodged_attacks']))}")

        print("DODGE")
        print(f"    Total nr times dodged: {sum(matches['dodged_attacks'])}")
        print(f"    Average nr dodges per match: {self.safe_divide(sum(matches['dodged_attacks']), len(matches))}")
        print(f"    Dodge rate: {self.safe_divide(sum(matches['dodged_attacks']), sum(matches['received_attacks']))}")

        print("MISSES")
        print(f"    Total nr times missed: {sum(matches['missed_attacks'])}")
        print(f"    Average nr misses per match: {self.safe_divide(sum(matches['missed_attacks']), len(matches))}")



import os
import re

import numpy as np
import pandas as pd
import sqlalchemy


class MatchParser:

    def __init__(self, gladiator_name, match_folder='../matches'):
        self.psql_engine = sqlalchemy.create_engine(f'postgresql+psycopg2://{os.getlogin()}@localhost/postgres')

        self.gladiator_name = gladiator_name
        self.match_folder = match_folder
        self.matches = None

        self.regex_match_type = open('regex/match_type.re').read().replace('\n', '')
        self.regex_match_summary = open('regex/match_summary.re').read().replace('\n', '')
        self.regex_total_damage = open('regex/total_damage.re').read().replace('\n', '')
        self.regex_total_damage_with_parries_blocks = open('regex/total_damage_with_parries_blocks.re').read().replace('\n', '')
        self.regex_higest_damage = open('regex/highest_damage.re').read().replace('\n', '')
        self.regex_received_damage = open('regex/received_damage.re').read().replace('\n', '')
        self.regex_received_attacks = open('regex/received_attacks.re').read().replace('\n', '')
        self.regex_dodged_attacks = open('regex/dodged_attacks.re').read().replace('\n', '')
        self.regex_dodged_attacks = open('regex/dodged_attacks.re').read().replace('\n', '')
        self.regex_partial_dodged_attacks = open('regex/partial_dodged_attacks.re').read().replace('\n', '')
        self.regex_parried_attacks = open('regex/parried_attacks.re').read().replace('\n', '')
        self.regex_blocked_attacks = open('regex/blocked_attacks.re').read().replace('\n', '')
        self.regex_partial_blocked_attacks = open('regex/partial_blocked_attacks.re').read().replace('\n', '')
        self.regex_missed_attacks = open('regex/missed_attacks.re').read().replace('\n', '')
        self.regex_partial_missed_attacks = open('regex/partial_missed_attacks.re').read().replace('\n', '')

    def __read_matches(self):
        matches = pd.DataFrame(
            data=[
                # [match_id, match_html]
                [f.split('.')[0], open(os.path.join(self.match_folder, f)).read()]
                for f in os.listdir(self.match_folder)
            ],
            columns=['match_id', 'match_html']
        )
        return matches

    def _parse_match_type(self, match_html):
        try:
            return re.findall(self.regex_match_type, match_html)[0].lower()
        except IndexError:
            return ""

    def _parse_summary(self, match_html):
        try:
            return re.findall(self.regex_match_summary.format(GLADIATOR_NAME=self.gladiator_name), match_html)[0]
        except IndexError:
            return ""

    def _parse_total_damage(self, summary_html):
        return self._parse_metric(summary_html, self.regex_total_damage)

    def _parse_total_damage_with_parries_blocks(self, summary_html):
        return self._parse_metric(summary_html, self.regex_total_damage_with_parries_blocks)

    def _parse_highest_damage(self, summary_html):
        return self._parse_metric(summary_html, self.regex_higest_damage)

    def _parse_received_damage(self, summary_html):
        return self._parse_metric(summary_html, self.regex_received_damage)

    def _parse_received_attacks(self, summary_html):
        return self._parse_metric(summary_html, self.regex_received_attacks)

    def _parse_dodged_attacks(self, summary_html):
        return self._parse_metric(summary_html, self.regex_dodged_attacks)

    def _parse_partial_dodged_attacks(self, summary_html):
        return self._parse_metric(summary_html, self.regex_partial_dodged_attacks)

    def _parse_parried_attacks(self, summary_html):
        return self._parse_metric(summary_html, self.regex_parried_attacks)

    def _parse_blocked_attacks(self, summary_html):
        return self._parse_metric(summary_html, self.regex_blocked_attacks)

    def _parse_partial_blocked_attacks(self, summary_html):
        return self._parse_metric(summary_html, self.regex_partial_blocked_attacks)

    def _parse_missed_attacks(self, summary_html):
        return self._parse_metric(summary_html, self.regex_missed_attacks)

    def _parse_partial_missed_attacks(self, summary_html):
        return self._parse_metric(summary_html, self.regex_partial_missed_attacks)

    def _parse_metric(self, summary_html, metric_regex):
        try:
            return int(re.findall(metric_regex, summary_html)[0])
        except IndexError:
            return np.NaN

    def parse_matches(self):
        # Open all matches
        matches = self.__read_matches()

        # Clean some shit away
        matches['match_html'] = matches['match_html'].apply(lambda html: html.replace('=\n', ''))

        # Get match type
        matches['match_type'] = matches['match_html'].apply(self._parse_match_type)

        # Get summary
        matches['match_summary'] = matches['match_html'].apply(self._parse_summary)

        # Get all individual metrics
        matches['total_damage'] = matches['match_summary'].apply(self._parse_total_damage)
        matches['total_damage_with_parries_blocks'] = matches['match_summary'].apply(self._parse_total_damage_with_parries_blocks)
        matches['highest_damage'] = matches['match_summary'].apply(self._parse_highest_damage)
        matches['received_damage'] = matches['match_summary'].apply(self._parse_received_damage)
        matches['received_attacks'] = matches['match_summary'].apply(self._parse_received_attacks)
        matches['dodged_attacks'] = matches['match_summary'].apply(self._parse_dodged_attacks)
        matches['partial_dodged_attacks'] = matches['match_summary'].apply(self._parse_partial_dodged_attacks)
        matches['parried_attacks'] = matches['match_summary'].apply(self._parse_parried_attacks)
        matches['blocked_attacks'] = matches['match_summary'].apply(self._parse_blocked_attacks)
        matches['partial_blocked_attacks'] = matches['match_summary'].apply(self._parse_partial_blocked_attacks)
        matches['missed_attacks'] = matches['match_summary'].apply(self._parse_missed_attacks)
        matches['partial_missed_attacks'] = matches['match_summary'].apply(self._parse_partial_missed_attacks)

        # Set match_id as index
        matches.set_index('match_id', inplace=True)

        # Persist matches
        self.matches = matches
        self.matches.to_sql('matches', con=self.psql_engine, if_exists='append')

        return self.matches

    def print_summary(self, matches=None):
        matches = matches if matches is not None else self.matches

        print()
        print(f"------------- SUMMARY -------------")
        print(f"Gladiator name: {gladiator_name}")
        print(f"Nr matches: {len(matches)}")
        for match_type in sorted(matches['match_type'].unique()):
            matches_of_type = matches[matches['match_type'] == match_type]
            print(f"Nr matches of type {match_type}: {len(matches_of_type)} ({100 * len(matches_of_type) / len(matches)}%)")

    def print_metrics_per_match_type(self, matches=None):
        matches = matches if matches is not None else self.matches

        for match_type in sorted(matches['match_type'].unique()):
            matches_of_type = matches[matches['match_type'] == match_type]

            print()
            print()
            print(f"------------- {match_type.upper()} -------------")
            print(f"Nr matches: {len(matches_of_type)}")
            print()

            self.print_metrics(matches=matches_of_type)

    def print_metrics(self, matches=None):
        matches = matches if matches is not None else self.matches

        print("GIVEN ATTACKS")
        print(f"    Total damage: {sum(matches['total_damage'])}")
        print(f"    Average damage per match: {sum(matches['total_damage']) / len(matches)}")

        print("RECEIVED ATTACKS")
        print(f"    Total damage received: {sum(matches['received_damage'])}")
        print(f"    Total nr received attacks: {sum(matches['received_attacks'])}")
        print(f"    Average damage received per match: {sum(matches['received_damage']) / len(matches)}")
        print(f"    Average nr received attacks per match: {sum(matches['received_attacks']) / len(matches)}")

        print("BLOCK")
        print(f"    Total nr times blocked: {sum(matches['blocked_attacks'])}")
        print(f"    Average nr blocks per match: {sum(matches['blocked_attacks']) / len(matches)}")
        print(f"    Block rate: {sum(matches['blocked_attacks']) / sum(matches['received_attacks'])}")

        print("DODGE")
        print(f"    Total nr times dodged: {sum(matches['dodged_attacks'])}")
        print(f"    Average nr dodges per match: {sum(matches['dodged_attacks']) / len(matches)}")
        print(f"    Dodge rate: {sum(matches['dodged_attacks']) / sum(matches['received_attacks'])}")

        print("MISSES")
        print(f"    Total nr times missed: {sum(matches['missed_attacks'])}")
        print(f"    Average nr misses per match: {sum(matches['missed_attacks']) / len(matches)}")


if __name__ == '__main__':
    gladiator_name = 'Master Pain'

    match_parser = MatchParser(gladiator_name)
    match_parser.parse_matches()

    match_parser.print_summary()
    match_parser.print_metrics_per_match_type()

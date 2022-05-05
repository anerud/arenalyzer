import os
import re

import numpy as np
import pandas as pd

from db_connector.db_connector import DBConnector
from tools.utils import read_relative_file_path, get_relative_file_path


class MatchParser:
    def __init__(self, gladiator_name, match_folder='../matches'):
        self.db_connector = DBConnector()

        self.gladiator_name = gladiator_name
        self.match_folder = match_folder
        self.matches = None

        self.regex_gladiator_level = read_relative_file_path('regex/gladiator_level.re').replace('\n', '')
        self.regex_match_type = read_relative_file_path('regex/match_type.re').replace('\n', '')
        self.regex_match_tactic = read_relative_file_path('regex/match_tactic.re').replace('\n', '')
        self.regex_match_summary = read_relative_file_path('regex/match_summary.re').replace('\n', '')
        self.regex_total_damage = read_relative_file_path('regex/total_damage.re').replace('\n', '')
        self.regex_total_damage_with_parries_blocks = read_relative_file_path('regex/total_damage_with_parries_blocks.re').replace('\n', '')
        self.regex_higest_damage = read_relative_file_path('regex/highest_damage.re').replace('\n', '')
        self.regex_received_damage = read_relative_file_path('regex/received_damage.re').replace('\n', '')
        self.regex_received_attacks = read_relative_file_path('regex/received_attacks.re').replace('\n', '')
        self.regex_dodged_attacks = read_relative_file_path('regex/dodged_attacks.re').replace('\n', '')
        self.regex_dodged_attacks = read_relative_file_path('regex/dodged_attacks.re').replace('\n', '')
        self.regex_partial_dodged_attacks = read_relative_file_path('regex/partial_dodged_attacks.re').replace('\n', '')
        self.regex_parried_attacks = read_relative_file_path('regex/parried_attacks.re').replace('\n', '')
        self.regex_blocked_attacks = read_relative_file_path('regex/blocked_attacks.re').replace('\n', '')
        self.regex_partial_blocked_attacks = read_relative_file_path('regex/partial_blocked_attacks.re').replace('\n', '')
        self.regex_missed_attacks = read_relative_file_path('regex/missed_attacks.re').replace('\n', '')
        self.regex_partial_missed_attacks = read_relative_file_path('regex/partial_missed_attacks.re').replace('\n', '')

    def __read_matches(self):
        match_files = os.listdir(get_relative_file_path(self.match_folder))
        match_ids = [f.split('.')[0] for f in match_files]
        new_match_ids = self.db_connector.get_nonexisting_matches(match_ids)
        new_matches = pd.DataFrame(
            data=[
                # [match_id, match_html]
                [self.gladiator_name, match_id, read_relative_file_path(os.path.join(self.match_folder, str(match_id) + '.mht'))]
                for match_id in new_match_ids
            ],
            columns=['gladiator_name', 'match_id', 'match_html']
        )
        return new_matches

    def __replace_characters(self, string):
        return string.replace('=c3=a4', 'ä').replace('=a3=a5', 'å')

    def _parse_gladiator_level(self, match_html):
        try:
            return self.__replace_characters(
                re.findall(
                    self.regex_gladiator_level.format(GLADIATOR_NAME=self.gladiator_name),
                    match_html
                )[0].lower()
            )
        except IndexError:
            return ""

    def _parse_match_type(self, match_html):
        try:
            return self.__replace_characters(re.findall(self.regex_match_type, match_html)[0].lower())
        except IndexError:
            return ""

    def _parse_match_tactic(self, match_html):
        try:
            return self.__replace_characters(re.findall(self.regex_match_tactic, match_html)[0].lower())
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

        # Get only files with gladiator_name
        matches = matches[matches['match_html'].str.contains(f'{self.gladiator_name}')]

        # Get match info
        #matches['gladiator_level'] = matches['match_html'].apply(self._parse_gladiator_level)
        matches['match_type'] = matches['match_html'].apply(self._parse_match_type)
        matches['match_tactic'] = matches['match_html'].apply(self._parse_match_tactic)

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

        # Cleanup
        matches.set_index('match_id', inplace=True)
        matches.drop('match_html', axis=1, inplace=True)  # Do not save entire html in database
        matches.drop('match_summary', axis=1, inplace=True)  # Do not save summary in database
        matches.dropna(inplace=True)

        # Persist matches
        self.matches = matches
        self.db_connector.persist_matches(self.matches)
        print(f"Persisted {len(self.matches)} new matches!")

        return self.matches


if __name__ == '__main__':
    matches = MatchParser(gladiator_name='Master Pain').parse_matches()
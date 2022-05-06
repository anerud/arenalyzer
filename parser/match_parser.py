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
        self.regex_gladiator_name = read_relative_file_path('regex/gladiator_name.re').replace('\n', '')
        self.regex_gladiator_level = read_relative_file_path('regex/gladiator_level.re').replace('\n', '')
        self.regex_match_type = read_relative_file_path('regex/match_type.re').replace('\n', '')
        self.regex_match_tactic = read_relative_file_path('regex/match_tactic.re').replace('\n', '')
        self.regex_match_summary = read_relative_file_path('regex/match_summary.re').replace('\n', '')
        self.regex_total_damage = read_relative_file_path('regex/total_damage.re').replace('\n', '')
        self.regex_total_damage_with_parries_blocks = read_relative_file_path('regex/total_damage_with_parries_blocks.re').replace('\n', '')
        self.regex_highest_damage = read_relative_file_path('regex/highest_damage.re').replace('\n', '')
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
                [match_id, read_relative_file_path(os.path.join(self.match_folder, str(match_id) + '.mht'))]
                for match_id in new_match_ids
            ],
            columns=['match_id', 'match_html']
        )
        return new_matches

    def __replace_characters(self, string):
        # TODO: Parse these in a better way
        return (
            string
                .replace('=\n', '')
                .replace('=A3=A5', 'Å')
                .replace('=A3=A4', 'Ä')
                .replace('=A3=B6', 'Ö')
                .replace('=C3=A4', '')
                .replace('=C3=A5', 'å')
                .replace('=C3=B6', 'ö')
        )

    def _parse_gladiator_level(self, match_html):
        try:
            return re.findall(self.regex_gladiator_level.format(GLADIATOR_NAME=self.gladiator_name), match_html)[0]
        except IndexError:
            return ""

    def _parse_text(self, match_html, text_regex):
        try:
            return re.findall(text_regex, match_html)[0]
        except IndexError:
            return ""

    def _parse_texts(self, match_html, text_regex):
        try:
            return re.findall(text_regex, match_html)
        except IndexError:
            return ""

    def _parse_number(self, summary_html, metric_regex):
        try:
            return int(re.findall(metric_regex, summary_html)[0])
        except IndexError:
            return np.NaN

    def __parse_matches(self, matches):
        # Clean some shit away
        matches['match_html'] = matches['match_html'].apply(self.__replace_characters)

        # Get only files with gladiator_name
        matches = matches[matches['match_html'].str.contains(f'{self.gladiator_name}')]

        # Get match info
        matches['match_type'] = matches['match_html'].apply(self._parse_text, args=[self.regex_match_type])
        matches['match_tactic'] = matches['match_html'].apply(self._parse_text, args=[self.regex_match_tactic])

        return matches

    def __parse_match_summary(self, matches):
        # Get summary
        match_summary = matches[['match_id', 'match_html']]
        match_summary['match_summary'] = match_summary['match_html'].apply(self._parse_texts, args=[self.regex_match_summary])
        match_summary = match_summary.explode('match_summary')

        # Get gladiator name
        match_summary['gladiator_name'] = match_summary['match_summary'].apply(self._parse_text, args=[self.regex_gladiator_name])

        # Get all individual metrics
        match_summary['total_damage'] = match_summary['match_summary'].apply(self._parse_number, args=[self.regex_total_damage])
        match_summary['total_damage_with_parries_blocks'] = match_summary['match_summary'].apply(self._parse_number, args=[self.regex_total_damage_with_parries_blocks])
        match_summary['highest_damage'] = match_summary['match_summary'].apply(self._parse_number, args=[self.regex_highest_damage])
        match_summary['received_damage'] = match_summary['match_summary'].apply(self._parse_number, args=[self.regex_received_damage])
        match_summary['received_attacks'] = match_summary['match_summary'].apply(self._parse_number, args=[self.regex_received_attacks])
        match_summary['dodged_attacks'] = match_summary['match_summary'].apply(self._parse_number, args=[self.regex_dodged_attacks])
        match_summary['partial_dodged_attacks'] = match_summary['match_summary'].apply(self._parse_number, args=[self.regex_partial_dodged_attacks])
        match_summary['parried_attacks'] = match_summary['match_summary'].apply(self._parse_number, args=[self.regex_parried_attacks])
        match_summary['blocked_attacks'] = match_summary['match_summary'].apply(self._parse_number, args=[self.regex_blocked_attacks])
        match_summary['partial_blocked_attacks'] = match_summary['match_summary'].apply(self._parse_number, args=[self.regex_partial_blocked_attacks])
        match_summary['missed_attacks'] = match_summary['match_summary'].apply(self._parse_number, args=[self.regex_missed_attacks])
        match_summary['partial_missed_attacks'] = match_summary['match_summary'].apply(self._parse_number, args=[self.regex_partial_missed_attacks])

        # Cleanup
        match_summary.set_index(['match_id', 'gladiator_name'], inplace=True)
        match_summary.drop('match_html', axis=1, inplace=True)  # Do not save entire html in database
        match_summary.drop('match_summary', axis=1, inplace=True)  # Do not save summary in database

        return match_summary

    def __persist_matches(self, matches):
        matches = matches.drop('match_html', axis=1)
        matches = matches.set_index('match_id')
        self.db_connector.persist_matches(matches)
        print(f"Persisted {len(matches)} new matches!")

    def __persist_match_summary(self, match_summaries):
        self.db_connector.persist_match_summaries(match_summaries)
        print(f"Persisted {len(match_summaries)} new match summaries!")

    def parse_matches(self):
        # Open and persist matches
        matches = self.__read_matches()
        matches = self.__parse_matches(matches)
        self.__persist_matches(matches)

        # Parse and persist match summary
        match_summary = self.__parse_match_summary(matches)
        self.__persist_match_summary(match_summary)

        return matches, match_summary


if __name__ == '__main__':
    matches, match_summaries = MatchParser(gladiator_name='Master Pain').parse_matches()

import pandas as pd
import sqlalchemy
import os

from tools.utils import read_relative_file_path


class DBConnector:
    # Table names
    TABLE_MATCHES = 'matches'

    # Queries
    QUERY_NONEXISTING_MATCHES = 'sql/nonexisting_matches.sql'
    QUERY_SELECT_MATCHES = 'sql/select_matches.sql'

    def __init__(self):
        self.psql_engine = sqlalchemy.create_engine(f"postgresql+psycopg2://{os.getlogin()}@localhost/postgres")
        pass

    def persist_matches(self, matches):
        matches.to_sql(DBConnector.TABLE_MATCHES, con=self.psql_engine, if_exists='append')

    def get_nonexisting_matches(self, match_ids):
        formatted_match_ids = ", ".join(str(match_id) for match_id in match_ids)
        query = read_relative_file_path(DBConnector.QUERY_NONEXISTING_MATCHES).format(MATCH_IDS=formatted_match_ids)
        return pd.read_sql(sql=query, con=self.psql_engine)['match_id']

    def get_matches(self, gladiator_name, min_level=1, max_level=99, max_nr_matches=10000):
        query = read_relative_file_path(DBConnector.QUERY_SELECT_MATCHES).format(
            GLADIATOR_NAME=gladiator_name,
            MIN_LEVEL=min_level,
            MAX_LEVEL=max_level,
            MAX_NR_MATCHES=max_nr_matches,
        )
        return pd.read_sql(sql=query, con=self.psql_engine)

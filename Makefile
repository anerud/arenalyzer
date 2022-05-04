all:
	pip install -r requirements.txt
	psql -d postgres -f db_connector/sql/init_db.sql

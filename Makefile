install:
	pip install -r requirements.txt
	psql -d postgres -f db_connector/sql/init_db.sql

reinstall:
	psql -d postgres -f db_connector/sql/drop_db.sql
	psql -d postgres -f db_connector/sql/init_db.sql

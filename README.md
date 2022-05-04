To setup, run following commands:
* brew install postgres
* pg_ctl -D /usr/local/var/postgres start
* make install


To reinstall, run following commands:
* make reinstall


Save a couple of matches in matches/
* Go to a match history in google chrome (example: https://beta.lanista.se/game/arena/battles/420350)
* Save page as
* name the file the match id (eg. 420350)
* Under "Format", make sure to select "Web page, Single file"
* Save in the matches/ folder


Run the script:
* python main.py


def home(data):
    "Look at game ID suffix to identify home team"
    Add categorical variable indicating home team


def week(data):
    "Look at game ID prefix to calculate days between games and identify week number"
    Add variable indicating week number

    
def play(data):
    "Look at offensive team and count number of plays run"
    Add play-level variable indicating number of plays run, resetting with each game

    
def playtype(self,data):
	"Look at description to identify type of play (run, pass, kickoff, punt, fg, ep)"
	Add play-level categorical variable
    #Play type
	if ('pass' in data.columns['description']) or ('sacked' in data.columns['description') or ('passed' in data.columns['description')
        data.playtype = 'pass'
    elif('yards' in data.columns['description') or ('yards.' in data.columns['description') or ('no gain' in data.columns['description')
        data.playtype = 'run'

def completion(data):
    "Look at playtype and yardsgained to see if pass was a successful completion"
    Add play-level binary variable

    
def twopts(data):
	"Look at description to identify whether a play was a 2pt conversion attempt"
	Add play-level binary variable
	

def firstdown_play(data):
	"Identify whether play resulted in a first down"
	Add play-level binary variable
	

def firstdown_series(data):
	"Identify whether there was a first down in the series"
	Add series-level binary variable
	
	
def yardsgained(self, data):
	"Looks at next play's yard-line to identify yards gained"
	Add play-level numeric variable indicating yards gained
    data.columns['yardsgained = 0']
    replace yardsgained = ydline[+1] - ydline if off[+1] = off


def pointsscored_play(data):
	"Looks at offscore/defscore & team ID to find points changes"
	Add play-level variable indicating points scored
	
	
def pointsscored_drive(data):
	"Looks at offscore/defscore at end of each series to see score changes"
	Add series-level variable indicating points scored
	

def won(data):
	"Looks at offscore/defscore at end of game to identify winner"
	Add game-level binary variable identifying winner
	

def turnover(data):
	"Looks at description to identify the type of penalty, if any"
	Add play-level categorical variable naming the penalty
	

def turnover_yards(data):
	"Looks at turnover and yardline to identify penalty impact"
	Add play-level variable indicating yards lost/gained by offense
	"""Look at offsetting/declined penalties later"""
	
	
def turnovers_game(data):
	"Looks at turnover variable to tabulate turnovers per-game"
	Game-level variable for off/def indicating number of turnovers
	

def  night_game(data):
    "Look at date and game order on that date to identify night games"
    Game-level binary variable indicating whether it is a night game
    """Look at weather (temp, precipitation) later"""


def east_west(data):
    "Look at game ID suffix and see if a east coast team is traveling to the west"
    Game-level binary variable indicating whether it is an east-to-west game

    
def west_east(data):
    "Look at game ID suffix and see if a west coast team is traveling to the east"
    Game-level binary vairable indicating whether it is a west-to-east game
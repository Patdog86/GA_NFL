import parse_gameid as pg
import play_parser 


class PlayRecord(object):

    def __init__(self, record_series):
        """
        Record series must be a Pandas series object.
        """

        self.series = record_series

    def description(self):
        return self.series['description']

    def gameid(self):
        return self.series['gameid']

    def set_game(self):
        self.date, self.matchup, self.awayteam, self.hometeam = pg.parse_gameid(self.gameid())

    def play(self):
        return play_parser.Play(self.description())

import pdb
import re

class Play(object):
    
    def __init__(self, play_text):
        self.play_text = play_text
        self.val = 'run'

    def __str__(self):
        return "<Play %s>" % self.val

    def play_type(self):
    	
        if('pass' in self.play_text) or ('sacked' in self.play_text) or ('passed' in self.play_text):
            self.val = 'pass'
        elif('yards' in self.play_text) or ('yards.' in self.play_text) or ('no gain' in self.play_text):
            self.val = 'run'
        elif re.search('kick', self.play_text):
            self.val = 'kick'
        
        return self.val
        
class Game(object):
    
    def __init__(self, game_records):
        """
        game_records is a list of all records for a particular game. e.g. they should each have the same game id"""
        self.game_records = game_records

    def home_team(self):
        val = self.game_records[0]
        return val['home']
        #-return val[3]
        #-return val.home_team()

class Record(object):
    """
    Represents a single record of a play, e.g. one line of data
    """
    
    def __init__(self, line):
        self.line = line
        
    def home_team(self):
        return self['home']

import doctest

def parse_gameid(gameid):
    """
    Parse a gameid string.

    The following is a doctest.  In this file, when doctest.testmod() is called
    (see if statement at bottom), items with docstrings and following '>>>' are
    run and their return compared with an expected value below.  The first of
    these should pass, the second is set up to fail.  Comment it out when you
    understand.

    The idea is to show what is returned by the tested function.


    >>> parse_gameid('20020905_SF@NYG')
    ('20020905', 'SF@NYG', 'SF', 'NYG')

    Demo a test failure
    >>> parse_gameid('20020905_SF@NYG')
    ('20020905', 'SF@NYG', 'DAL', 'NYG')


    """

    date, matchup = gameid.split('_')
    awayteam, hometeam = matchup.split('@')
    return date, matchup, awayteam, hometeam


if __name__ == '__main__':
    doctest.testmod()

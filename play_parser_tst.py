import unittest2

import play_parser as pp

class PlayParserTest(unittest2.TestCase):

    def setUp(self):
        self.p1 = pp.Play("J.Cortez kicks 75 yards from SF 30 to NYG -5. R.Dixon  Touchback.")
        self.p2 = pp.Play("(15:00) T.Barber left end to NYG 24 for 4 yards (C.Okeafor  J.Webster).")
        self.p3 = pp.Play("(14:25) K.Collins pass incomplete to J.Shockey (D.Smith).")

    def test_play_type(self):
        self.assertEqual(self.p1.play_type(), 'kick')
        self.assertEqual(self.p2.play_type(), 'run')
        self.assertEqual(self.p3.play_type(), 'pass')


#   EXAMPLE OF PLAY DESCRIPTIONS:
"""
J.Cortez kicks 75 yards from SF 30 to NYG -5. R.Dixon  Touchback.
(15:00) T.Barber left end to NYG 24 for 4 yards (C.Okeafor  J.Webster).
(14:25) K.Collins pass incomplete to J.Shockey (D.Smith).
(14:20) PENALTY on NYG-J.Shockey  False Start  5 yards  enforced at NYG 24 - No Play.
(14:20) (Shotgun) K.Collins pass intended for T.Barber INTERCEPTED by T.Parrish (M.Rumph) at NYG 29. T.Parrish to NYG 23 for 6 yards (T.Barber).
(14:09) J.Garcia right end ran ob at NYG 7 for 16 yards (B.Short). Back to pass  rushes.
(13:38) PENALTY on SF-R.Stone  False Start  5 yards  enforced at NYG 7 - No Play.
(13:35) G.Hearst left guard to NYG 8 for 4 yards (C.Griffin).
(12:47) J.Garcia pass incomplete to T.Owens.
(12:40) J.Garcia pass to G.Hearst to NYG 7 for 1 yard (J.Sehorn  S.Williams).
(11:59) J.Cortez 25 yard field goal is BLOCKED (M.Rosenthal)  Center-B.Jennings  Holder-J.Baker.
(11:51) K.Collins pass to A.Toomer pushed ob at NYG 22 for 2 yards (J.Webster).
(11:23) K.Collins pass incomplete to A.Toomer. PENALTY on SF-J.Webster  Defensive Pass Interference  5 yards  enforced at NYG 22 - No Play.

"""


if __name__ == '__main__':
    unittest2.main()



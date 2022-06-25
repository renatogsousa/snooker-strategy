import auxiliary

class Player:
    players_features = {
        'debug': {
            'pot_success': [10, 10, 10, 10, 10],  # pot success (%) of shots 1-5 (1 easy, 5 hard)
            'offensive': [100, 100, 90, 75, 50],  # probability (%) to attack shots 1-5 (1 easy, 5 hard)
            'cueball_control': [95, 95, 95, 75, 50],
            # cue ball control success (%) on shots 1-5 (1- easy, 5 hard)
            'defensive': 90  # success (%) on defensive shots
        },
        'world_snooker': {
            'pot_success': [99, 92, 85, 70, 60],  # pot success (0-1) of shots 1-5 (1 easy, 5 hard)
            'offensive': [100, 100, 90, 75, 50],  # probability (0-1) to attack shots 1-5 (1 easy, 5 hard)
            'cueball_control': [95, 95, 95, 75, 50],   # cue ball control success (0-1) on shots 1-5 (1- easy, 5 hard)
            'defensive': 90 #success (0-1) on defensive shots
        },
        'portuguese_high': {
            'pot_success': [90, 70, 60, 40, 30],  # pot success (0-1) of shots 1-5 (1 easy, 5 hard)
            'offensive': [100, 100, 90, 75, 50],  # probability (0-1) to attack shots 1-5 (1 easy, 5 hard)
            'cueball_control': [90, 80, 50, 20, 10],   # cue ball control success (0-1) on shots 1-5 (1- easy, 5 hard)
            'defensive': 50  # success (0-1) on defensive shots
        },
        'portuguese_low': {
            'pot_success': [80, 55, 40, 25, 10],  # pot success (0-1) of shots 1-5 (1 easy, 5 hard)
            'offensive': [90, 90, 50, 20, 10],  # probability (0-1) to attack shots 1-5 (1 easy, 5 hard)
            'cueball_control': [50, 30, 20, 10, 5], # cue ball control success (0-1) on shots 1-5 (1- easy, 5 hard)  # percentage of cue ball control success
            'defensive': 20  # success (0-1) on defensive shots
        }

    }

    def __init__(self, name=None, standard=None):

        self.name = name if name is not None else "player"
        self.points = 0
        self.all_breaks = []  # list of breaks during a frame
        self.current_break = []  # list of balls in current break
        self.current_ball = "R"  # R for red, C for color
        self.pot_success = []
        self.offensive = []
        self.cueball_control = []
        self.defensive = 0
        self.frameattacks = []   # history of attack (s,1) defense (s,0) decisions along a frame, s is shot difficulty
        self.framepots = []     # historry of pots (s,1) or misses (s,0) when decided to attack, s is shot difficulty
        self.framecuecontrol = [] # history of cue control (s,1) or missed control (s,0) when potting a ball with s difficulty
        self.framedefenses = [] # history of success defensive shots (s,1) or not success (s,0) when not deciding to attack

        # set player characteristics, if none will set as world snooker
        match standard:

            case 0:
                self.setplayer('debug')
            case 1:
                self.setplayer('world_snooker')
            case 2:
                self.setplayer('portuguese_high')
            case 3:
                self.setplayer('portuguese_low')
            case _:
                self.setplayer('world_snooker')





    def reset_data(self):
        self.points = 0
        self.current_break = []
        self.all_breaks = []
        self.current_ball = 'R'
        self.frameattacks = []
        self.framepots = []
        self.framecuecontrol = []
        self.framedefenses = []


    def reset_break(self):
        if len(self.current_break)==0:
            return
        else:
            self.all_breaks.append(self.current_break)
            self.current_break = []

    def pot_ball(self, ball):
        self.current_break.append(ball)
        if ball == "R":
            self.points += 1
        else:
            self.points += 4.5

    def setplayer(self, player_key):
        # need to put [:] or create a copy of the list otherwise all players from same category would link to same list
        self.pot_success = Player.players_features[player_key]['pot_success'][:]
        self.offensive = Player.players_features[player_key]['offensive'][:]
        self.cueball_control = Player.players_features[player_key]['cueball_control'][:]
        self.defensive = Player.players_features[player_key]['defensive']

    def attacks(self, shot_difficulty):
        # shot difficulty 1-easy to 5- hard
        prob = self.offensive[shot_difficulty-1]
        # return true if player will attack or false if will defend, depending on the probability of player attacking
        # certain shots, defined in it's offensive statistics
        return auxiliary.sample_event(prob)

    def pots(self, shot_difficulty):
        # shot difficulty 1-easy to 5- hard
        # return true if player pots the ball or false if will fail, depending on the player pot success probability
        prob = self.pot_success[shot_difficulty - 1]
        return auxiliary.sample_event(prob)

    def controls_cueball(self, shot_difficulty):
        # return true if cueball was controlled (easier next shot) false if not (harder next shot)
        prob = self.cueball_control[shot_difficulty - 1]
        return auxiliary.sample_event(prob)

    def defends(self):
        prob = self.defensive
        return auxiliary.sample_event(prob)

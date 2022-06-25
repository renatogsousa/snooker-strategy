import auxiliary
import player
import random


class Frame:
    shot_diff_list = [1, 2, 3, 4, 5]  # possible shot difficulty levels 1-easy, 5-hard

    def __init__(self, p1=None, p2=None, n_reds=None):

        self.players = (p1, p2) if p1 is not None and p2 is not None else (player.Player(), player.Player())
        self.n_reds = n_reds if n_reds is not None else 15
        self.current_player = self.players[0]

        self.table_balls = ['C', 'C', 'C', 'C', 'C', 'C']
        self.table_balls.extend(n_reds * ['R'])
        self.ball_on = 'R'
        self.shot_difficulty = 1
        self.final_sequence = False

    def start(self, p=None, deb=False):
        pl = p if p is not None else 0
        self.set_player(pl)  # sets starting player if chosen or selects random

        # reset player's scores and breaks
        for pla in self.players:
            pla.reset_data()

        # assume break off is made and no ball is potted
        self.swap_player()

        # second ball difficulty will be random, from 1-5
        self.shot_difficulty = auxiliary.random_from(Frame.shot_diff_list)

        play = 0
        while len(self.table_balls) > 0:  # proceed game, while there are balls on the table
            play += 1

            self.set_ball_on()  # defines if ball on is red 'R' or color 'C'
            self.check_final_sequence()  # check if we are playing final sequence of colors
            # debug info
            if deb:
                print("play:", play)
                print("number of balls on table:", len(self.table_balls))
                print("current player:", self.current_player.name)
                print("ball on:", self.ball_on)
                print("shot difficulty:", self.shot_difficulty)

            if self.current_player.attacks(self.shot_difficulty):

                if deb: print("Attacks")

                # add to statistics of attacks
                self.current_player.frameattacks.append((self.shot_difficulty, 1))

                # what happens if player tries to pot
                if self.current_player.pots(self.shot_difficulty):
                    if deb: print("Pots")

                    #add to frame statistics of pot as success
                    self.current_player.framepots.append((self.shot_difficulty, 1))

                    # if player pots ball on
                    # add points to current player and add ball to break
                    self.current_player.pot_ball(self.ball_on)
                    # if was a red ball, remove from balls on table
                    if self.ball_on == 'R':
                        self.table_balls.remove('R')
                        # else, if it was a color ball, remove if we're in the final sequence, otherwise, let it
                    else:
                        if self.final_sequence:
                            self.table_balls.remove('C')

                    # update next shot difficulty
                    if self.current_player.controls_cueball(self.shot_difficulty):

                        # add to frame statistics of cue ball control as success
                        self.current_player.framecuecontrol.append((self.shot_difficulty, 1))

                        # if controlled cue ball next shot difficulty <= current shot difficulty
                        self.shot_difficulty = auxiliary.random_from(Frame.shot_diff_list[:self.shot_difficulty])
                    else:

                        # add to frame statistics of cue ball control as failure
                        self.current_player.framecuecontrol.append((self.shot_difficulty, 0))

                        # if couldn't control cue ball, next shot is random difficulty
                        self.shot_difficulty = auxiliary.random_from(Frame.shot_diff_list)

                else:
                    if deb: print("Missed")

                    #add to statistics of pots as missed
                    self.current_player.framepots.append((self.shot_difficulty, 0))

                    # if player misses ball on next shot difficulty for opponent is random
                    self.shot_difficulty = auxiliary.random_from(Frame.shot_diff_list)
                    # reset current player break and swap player
                    self.swap_player()


            else:
                #add to attack/defense statistics
                self.current_player.frameattacks.append((self.shot_difficulty, 0))

                # what happens if player plays defensive shot
                # if player succeeds in defensive shot, next shot difficulty is random between [4,5] else between [1,2,3]
                if self.current_player.defends():

                    # add to frame defensive statistics as success
                    self.current_player.framedefenses.append((self.shot_difficulty, 1))

                    if deb: print("Defends well")
                    self.shot_difficulty = auxiliary.random_from(Frame.shot_diff_list[-2:])
                else:
                    if deb: print("Defends badly")

                    # add to frame defensive statistics as failure
                    self.current_player.framedefenses.append((self.shot_difficulty, 0))

                    self.shot_difficulty = auxiliary.random_from(Frame.shot_diff_list[:3])

                # reset current player break and swap players
                self.swap_player()

            # end of game
        self.show_winner()
        self.show_stats()

    def set_player(self, p=None):
        # p should 1 for player 1 or 2 for player 2, else random player will be selected
        if p == 1 or p == 2:
            self.current_player = self.players[p - 1]
        else:
            temp = random.random()
            if temp < 0.5:
                self.current_player = self.players[0]
            else:
                self.current_player = self.players[1]

    def swap_player(self):
        # reset current player break
        self.current_player.reset_break()
        self.current_player = self.players[0] if self.current_player == self.players[1] else self.players[1]

    def show_winner(self):
        if self.players[0].points == self.players[1].points:
            winner = None
        else:
            winner = self.players[0] if self.players[0].points > self.players[1].points else self.players[1]
        print('Winner: ', winner.name)

    def show_stats(self):

        for p in self.players:
            print('###################')
            print(p.name, " points:", p.points)
            print("Breaks")
            for br in p.all_breaks:
                print(br)
            print('###################')

    def set_ball_on(self):
        # assuming there are balls on the table since it is within while loop
        if 'R' not in self.table_balls:
            self.ball_on = 'C'

        else:
            if len(self.current_player.current_break) == 0:  # first shot of the break -> red ball
                self.ball_on = 'R'
            else:
                if self.current_player.current_break[-1] == 'R':  # else, check what color was last ball
                    self.ball_on = 'C'
                else:
                    self.ball_on = 'R'

    def check_final_sequence(self):
        if 'R' not in self.table_balls:  # if there are no Reds, check if player just played last red
            if len(self.current_player.current_break) > 0 and self.current_player.current_break[-1] == 'R':
                self.final_sequence = False
            else:
                self.final_sequence = True

        else:
            self.final_sequence = False

    def restart(self):
        # reset table data
        self.table_balls = ['C', 'C', 'C', 'C', 'C', 'C']
        self.table_balls.extend(self.n_reds * ['R'])
        self.start()

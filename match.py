import frame
import matplotlib.pyplot as plt
import player


def get_frame_percentage(matchraw, frameindex):
    # first frame index is 0
    # each frame has a list of tuples (s, t/f)  with shot difficulty and if success or not on that statistic
    # matchraw is a list of frame raw statistics for one specific feature

    frame_stats = [[0, 0], [0, 0], [0, 0], [0, 0],
                   [0, 0]]  # [[diff_1success, diff_1failed], [diff_2success, diff_2failed] ]...

    for event in matchraw[frameindex]:  # frame 1 stats are in index 0...
        if event[1] == 1:
            frame_stats[event[0] - 1][0] += 1  # add one success to respective shot difficulty stats
        else:
            frame_stats[event[0] - 1][1] += 1  # add one failure to respective shot difficulty stats

    return frame_stats


def get_frame_breaks(breaks_list):
    # breaks_list from ome frame: [ ['R', 'C', 'R'], ['C', C', C'] ...

    breaks = []
    for br in breaks_list:
        reds = br.count('R')
        colors = br.count('C')
        breaks.append(reds + 4.5*colors)

    breaks.sort(reverse=True)

    return breaks


class Match:

    def __init__(self, p1, p2, n_frames, n_reds):

        self.p1 = p1
        self.p2 = p2
        self.n_frames = n_frames
        self.n_reds = n_reds
        self.p1stats = dict(points=[], breaks=[], pot_success=[], attacks=[], white_control=[], defense_success=[])
        self.p2stats = dict(points=[], breaks=[], pot_success=[], attacks=[], white_control=[], defense_success=[])
        self.p1_resume_stats = []  # will add here list of game (index 0) and each frane (index i) stats for player 1
        self.p2_resume_stats = []  # will add here list of game (index 0) and each frane (index i) stats for player 2
        self.full_match_stats = [] # will add here stats of full match frames

    def start_match(self):
        # reset players data
        self.reset_match()

        # create frame
        f = frame.Frame(self.p1, self.p2, self.n_reds)

        for n in range(self.n_frames):
            f.restart()

            # add frame statistics to match
            self.p1stats['attacks'].append(self.p1.frameattacks)
            self.p1stats['pot_success'].append(self.p1.framepots)
            self.p1stats['white_control'].append(self.p1.framecuecontrol)
            self.p1stats['defense_success'].append(self.p1.framedefenses)
            self.p1stats['points'].append(self.p1.points)
            self.p1stats['breaks'].append(self.p1.all_breaks)

            self.p2stats['attacks'].append(self.p2.frameattacks)
            self.p2stats['pot_success'].append(self.p2.framepots)
            self.p2stats['white_control'].append(self.p2.framecuecontrol)
            self.p2stats['defense_success'].append(self.p2.framedefenses)
            self.p2stats['points'].append(self.p2.points)
            self.p2stats['breaks'].append(self.p2.all_breaks)

        self.all_frames_stats()
        self.final_stats()
        print("match finished")

    def reset_match(self):
        self.p1.reset_data()
        self.p2.reset_data()
        self.p1stats = {'points': [],  # list of points per frame
                        'breaks': [],  # list of breaks per frame. each frame has a list of breaks
                        'pot_success': [],  # for each frame, a list of events with (s,1/0) where s is shot difficulty
                        'attacks': [],
                        'white_control': [],
                        'defense_success': []
                        }
        self.p2stats = {'points': [],
                        'breaks': [],
                        'pot_success': [],
                        'attacks': [],
                        'white_control': [],
                        'defense_success': []
                        }

        self.p1_resume_stats = []  # will add here list of game (index 0) and each frane (index i) stats for player 1
        self.p2_resume_stats = []  # will add here list of game (index 0) and each frane (index i) stats for player 2

    def all_frames_stats(self):

        # reset full match statistics
        self.p1_resume_stats = []
        self.p2_resume_stats = []

        played_frames = len(self.p1stats['points'])
        for f in range(played_frames):
            # add to full match statistics a list of dictionaries with individual frame statistics
            self.p1_resume_stats.append({'points': self.p1stats['points'][f],
                                         'breaks': get_frame_breaks(self.p1stats['breaks'][f]),
                                         'pot_success': get_frame_percentage(self.p1stats['pot_success'], f),
                                         'attacks': get_frame_percentage(self.p1stats['attacks'], f),
                                         'white_control': get_frame_percentage(self.p1stats['white_control'], f),
                                         'defense_success': get_frame_percentage(self.p1stats['defense_success'], f),
                                         })

            self.p2_resume_stats.append({'points': self.p2stats['points'][f],
                                         'breaks': get_frame_breaks(self.p2stats['breaks'][f]),
                                         'pot_success': get_frame_percentage(self.p2stats['pot_success'], f),
                                         'attacks': get_frame_percentage(self.p2stats['attacks'], f),
                                         'white_control': get_frame_percentage(self.p2stats['white_control'], f),
                                         'defense_success': get_frame_percentage(self.p2stats['defense_success'], f),
                                         })

    def final_stats(self):
        self.full_match_stats = []
        p1_full_stats = dict(frames_won=0, points=0, pot_success=[[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]],
                             attacks=[[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]],
                             white_control=[[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]],
                             defense_success=[[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]])

        p2_full_stats = dict(frames_won=0, points=0, pot_success=[[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]],
                             attacks=[[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]],
                             white_control=[[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]],
                             defense_success=[[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]])

        # points
        p1_full_stats['points'] = sum(self.p1stats['points'])
        p2_full_stats['points'] = sum(self.p2stats['points'])

        # highest break
        p1_max_break = 0
        p2_max_break = 0

        for fr in range(len(self.p1stats['points'])):
            # frame winner
            if self.p1_resume_stats[fr]['points'] != self.p2_resume_stats[fr]['points']:
                if self.p1_resume_stats[fr]['points'] > self.p2_resume_stats[fr]['points']:
                    p1_full_stats['frames_won'] += 1
                else:
                    p2_full_stats['frames_won'] += 1

            # max break
            if len(self.p1_resume_stats[fr]['breaks']) > 0:  # if player didn't score, breaks list might be empty no need to update max break
                if max(self.p1_resume_stats[fr]['breaks']) > p1_max_break:
                    p1_max_break = max(self.p1_resume_stats[fr]['breaks'])

            if len(self.p2_resume_stats[fr]['breaks']) > 0:  # if player didn't score, breaks list might be empty no need to update max break
                if max(self.p2_resume_stats[fr]['breaks']) > p2_max_break:
                    p2_max_break = max(self.p2_resume_stats[fr]['breaks'])


            # for other stats, sum from all breaks ['pot_success', 'attacks', 'white_control', 'defense_success']
            for k in ['pot_success', 'attacks', 'white_control', 'defense_success']:
                self.update_stats(p1_full_stats, self.p1_resume_stats[fr], k)
                self.update_stats(p2_full_stats, self.p2_resume_stats[fr], k)

        self.full_match_stats.append(p1_full_stats)
        self.full_match_stats.append(p2_full_stats)

    def update_stats(self, player_full_stats, frame_stats, parameter):
        for shot_difficulty in range(5):
            player_full_stats[parameter][shot_difficulty][0] += frame_stats[parameter][shot_difficulty][0]
            player_full_stats[parameter][shot_difficulty][1] += frame_stats[parameter][shot_difficulty][1]

    def plot_match_stats (self, pl, stats):
        """
        :param pl: player number 1/2
        :param stats: string from 'pot_success', 'attacks', 'white_control', 'defense_success'
        :return:
        """

        fig, ax = plt.subplots()
        yes = []
        no = []
        indexes = [1, 2, 3, 4, 5]

        data = self.full_match_stats[pl-1][stats]

        for shot in data:
            yes.append(shot[0])
            no.append(shot[1])

        p1 = ax.barh(indexes, yes, 0.35, label="yes", color="green")
        p2 = ax.barh(indexes, no, 0.35, left=yes, label='no', color="red")
        ax.set_ylabel('Shot difficulty')
        ax.set_xlabel('Events')
        ax.set_title('Player' + str(pl) + ': ' + stats)
        ax.legend()

        # Label with label_type 'center' instead of the default 'edge'
        ax.bar_label(p1, label_type='center')
        ax.bar_label(p2, label_type='center')
        ax.bar_label(p2)

        return fig

    def match_resume(self):

        print('Player:' + self.p1.name)
        print('Frames won:' + str(self.full_match_stats[0]['frames_won']))
        print('Total points:' + str(self.full_match_stats[0]['points']))

        print('Player:' + self.p2.name)
        print('Frames won:' + str(self.full_match_stats[1]['frames_won']))
        print('Total points:' + str(self.full_match_stats[1]['points']))

    def get_match_resume(self):

        resume1 = ""
        resume1 += 'Player:' + self.p1.name + '\n'
        resume1 += 'Frames won:' + str(self.full_match_stats[0]['frames_won']) + '\n'
        resume1 += 'Total points:' + str(self.full_match_stats[0]['points']) + '\n'
        resume2 = ""
        resume2 += 'Player:' + self.p2.name +'\n'
        resume2 += 'Frames won:' + str(self.full_match_stats[1]['frames_won']) + '\n'
        resume2 += 'Total points:' + str(self.full_match_stats[1]['points']) + '\n'
        return [resume1, resume2]



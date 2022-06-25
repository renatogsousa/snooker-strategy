import random
import matplotlib.pyplot as plt


def sample_event(prob):
    # simulates an event with prob probability to happen
    r = random.random()  #0-1 random value
    return r <= prob/100  # return true if random value is below or equal to probability, false if above probability


def random_from(mylist):
    # picks a random elemet from a list
    return mylist[random.randrange(len(mylist))]


def bar_shots_data(data, lab):
    fig, ax = plt.subplots()
    yes = []
    no = []
    indexes = [1, 2, 3, 4, 5]

    for shot in data:
        yes.append(shot[0])
        no.append(shot[1])

    p1 = ax.barh(indexes, yes, 0.35, label="yes")
    p2 = ax.barh(indexes, no, 0.35, left=yes, label='no')
    ax.set_ylabel('Shot difficulty')
    ax.set_xlabel('Events')
    ax.set_title(lab)
    ax.legend()

    # Label with label_type 'center' instead of the default 'edge'
    ax.bar_label(p1, label_type='center')
    ax.bar_label(p2, label_type='center')
    ax.bar_label(p2)

def rgb_hack(rgb):
    return "#%02x%02x%02x" % rgb
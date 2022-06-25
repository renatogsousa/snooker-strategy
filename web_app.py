import streamlit as st
import pandas as pd
import numpy as np

import player
import match

global m
global updated_match

def getdata(player):
    playerdict = {'pot success':player.pot_success, 'offensive':player.offensive, 'cue ball control':player.cueball_control, 'defensive': player.defensive}
    temp = pd.DataFrame(playerdict, [1, 2, 3, 4, 5])

    return temp

def start_match():
    global m
    global player1
    global player2
    global n_frames
    global n_reds

    m = match.Match(player1, player2, n_frames=n_frames, n_reds=n_reds)
    m.start_match()
    st.session_state['my_m'] = m
    set_updated_match(True)

    #st.text(m.get_match_resume())

def set_updated_match(bol):
    global updated_match
    updated_match = bol
    st.session_state['updated'] = updated_match


def get_resume():

    if st.session_state['my_m'] is not None:
        m = st.session_state['my_m']
        return m.get_match_resume()


def get_plot(player, statistic):
    if st.session_state['my_m'] is not None:
        m = st.session_state['my_m']
        return m.plot_match_stats(player, statistic)

def change_player_name(pl):
    if st.session_state['my_m'] is not None:
        m = st.session_state['my_m']

        if pl==1:
            plname = st.session_state['pl1_name']
            m.p1.name = plname
        else:
            plname = st.session_state['pl2_name']
            m.p2.name = plname


def update_pl(pl, k, shot):
    if st.session_state['my_m'] is not None:
        m = st.session_state['my_m']
        playerlist = [m.p1, m.p2]
        locplayer = playerlist[pl-1]

        if k == 'pots':
            locplayer.pot_success[shot] = st.session_state[k + str(pl) + '_' + str(shot + 1)]
        elif k == 'of':
            locplayer.offensive[shot] = st.session_state[k + str(pl) + '_' + str(shot + 1)]
        elif k == 'cc':
            locplayer.cueball_control[shot] = st.session_state[k + str(pl) + '_' + str(shot + 1)]
        elif k == 'def':
            locplayer.defensive = st.session_state[k + str(pl)]
    set_updated_match(False)

## match is updated if started and no further change in settings. otherwise variable will be false and no statistics can be shown
if 'updated' not in st.session_state.keys():
    updated_match = False
    st.session_state['updated'] = updated_match
else:
    updated_match = st.session_state['updated']


st.title('Snooker Strategy')
st.subheader('Match setup')


if 'player1' not in st.session_state.keys():
    player1 = player.Player("Ronnie", 1)
    st.session_state['player1'] = player1
else:
    player1 = st.session_state['player1']

if 'player2' not in st.session_state.keys():
    player2 = player.Player("Trump", 1)
    st.session_state['player2'] = player2
else:
    player2 = st.session_state['player2']

# edit player1  data
c1, c2 = st.columns([1, 1])


if c1.checkbox('Edit player 1', key='edit_pl1'):
    c11, c21 = st.columns([1, 1])
    with c11:
        edit_feature = st.selectbox('Feature of Player 1', ('Pot success', 'Offensive', 'Cue ball control', 'Safety'), key='sel1')


    with c21:

        if edit_feature == 'Pot success':
            slider_list = list()
            for shot_diff in range(5):
                slider_list.append(st.slider('Shots difficulty ' + str(shot_diff+1), 0, 100, value=player1.pot_success[shot_diff],
                                              step=1, key='pots1_' + str(shot_diff+1), on_change=update_pl, kwargs={'pl': 1, 'k': 'pots', 'shot': shot_diff}, help='Success %'))
        if edit_feature == 'Offensive':
            slider_list = list()
            for shot_diff in range(5):
                slider_list.append(st.slider( 'Shots difficulty ' + str(shot_diff+1), 0, 100, value=player1.offensive[shot_diff],
                                              step=1, key='of1_' + str(shot_diff+1), on_change=update_pl, kwargs={'pl': 1, 'k': 'of', 'shot': shot_diff}, help='Success %'))
        if edit_feature == 'Cue ball control':
            slider_list = list()
            for shot_diff in range(5):
                slider_list.append(st.slider( 'Shots difficulty ' + str(shot_diff+1), 0, 100, value=player1.cueball_control[shot_diff],
                                              step=1, key='cc1_' + str(shot_diff+1), on_change=update_pl, kwargs={'pl': 1, 'k': 'cc', 'shot': shot_diff}, help='Success %'))
        if edit_feature == 'Safety':
            slider_def = st.slider( 'Safety', 0, 100, value=player1.defensive, step=1, key='def1', on_change=update_pl, kwargs={'pl': 1, 'k': 'def', 'shot': 1}, help='Success %')


# edit player2 data
#c1, c2 = st.columns([1, 1])


if c2.checkbox('Edit player 2', key='edit_pl2'):
    c21, c22 = st.columns([1, 1])
    with c21:
        edit_feature = st.selectbox('Feature of Player 2', ('Pot success', 'Offensive', 'Cue ball control', 'Safety'), key='sel2')


    with c22:

        if edit_feature == 'Pot success':
            slider_list2 = list()
            for shot_diff in range(5):
                slider_list2.append(st.slider( 'Shots difficulty ' + str(shot_diff+1), 0, 100, value=player2.pot_success[shot_diff],
                                               step=1, key='pots2_' + str(shot_diff+1), on_change=update_pl, kwargs={'pl': 2, 'k': 'pots', 'shot': shot_diff}, help='Success %'))
        if edit_feature == 'Offensive':
            slider_list2 = list()
            for shot_diff in range(5):
                slider_list2.append(st.slider( 'Shots difficulty ' + str(shot_diff+1), 0, 100, value=player2.offensive[shot_diff],
                                               step=1, key='of2_' + str(shot_diff+1), on_change=update_pl, kwargs={'pl': 2, 'k': 'of', 'shot': shot_diff}, help='Success %'))
        if edit_feature == 'Cue ball control':
            slider_list2 = list()
            for shot_diff in range(5):
                slider_list2.append(st.slider( 'Shots difficulty ' + str(shot_diff+1), 0, 100, value=player2.cueball_control[shot_diff],
                                               step=1, key='cc2_' + str(shot_diff+1), on_change=update_pl, kwargs={'pl': 2, 'k': 'cc', 'shot': shot_diff}, help='Success %'))
        if edit_feature == 'Safety':
            slider_def2 = st.slider( 'Safety', 0, 100, value=player2.defensive, step=1, key='def2', on_change=update_pl, kwargs={'pl': 2, 'k': 'def', 'shot': 1}, help='Success %')

# can also write to columns with, col1.write(data) for example
col1, col2 = st.columns([1, 1])

with col1:
    pl1_name = st.text_input('Player 1', value=player1.name, on_change=change_player_name, kwargs={'pl': 1}, key='pl1_name')
    if st.checkbox('Show player 1 profile', key='pl1'):
        st.write(getdata(player1))


with col2:
    pl2_name = st.text_input('Player 2', value = player2.name, on_change=change_player_name,kwargs={'pl':2}, key='pl2_name')
    if st.checkbox('Show player 2 profile', key='pl2'):
        st.write(getdata(player2))

n_reds = st.radio('Nr of reds', [15, 10, 6], on_change=set_updated_match, kwargs={'bol': False})

n_frames = st.number_input('Nr of frames', 1, 35, step=1, on_change=set_updated_match, kwargs={'bol': False})

press_start = st.button('Start match', key='buttonstart', on_click=start_match)


if updated_match:

    st.subheader('Match Statistics')

    if st.checkbox('Match resume', key='match_resume'):
        col_1, col_2 = st.columns([1, 1])
        resume = get_resume()
        with col_1:
            st.text(resume[0])
        with col_2:
            st.text(resume[1])



    if st.checkbox('Offensive shots', key='off_stats'):
        col_1, col_2 = st.columns([1, 1])
        with col_1:
            st.write(get_plot(1, 'attacks'))
        with col_2:
            st.write(get_plot(2, 'attacks'))

    if st.checkbox('Pot success', key='pot_stats'):
        col_1, col_2 = st.columns([1, 1])
        with col_1:
            st.write(get_plot(1, 'pot_success'))
        with col_2:
            st.write(get_plot(2, 'pot_success'))

    if st.checkbox('Cue ball control', key='cue_control_stats'):
        col_1, col_2 = st.columns([1, 1])
        with col_1:
            st.write(get_plot(1, 'white_control'))
        with col_2:
            st.write(get_plot(2, 'white_control'))

    if st.checkbox('Safety success', key='safety_stats'):
        col_1, col_2 = st.columns([1, 1])
        with col_1:
            st.write(get_plot(1, 'defense_success'))
        with col_2:
            st.write(get_plot(2, 'defense_success'))


#create match if not existing

if 'my_m' not in st.session_state.keys():
    m = match.Match(player1, player2, n_frames=n_frames, n_reds=n_reds)
    st.session_state['my_m'] = m

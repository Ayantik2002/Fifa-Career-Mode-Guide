import streamlit as st
import pickle
from scipy.spatial.distance import euclidean


new_df = pickle.load(open('new_df.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))


def recommend(player):
    player_index = new_df[new_df['short_name'] == player].index[0]
    distances = similarity[player_index]
    player_list = sorted(list(enumerate(distances)), key=lambda x: x[1])[1:]

    expensive = []
    e_cnt = 0
    medium = []
    m_cnt = 0
    cheap = []
    c_cnt = 0

    most_alike = []
    a_cnt = 0

    for i in player_list:
        if a_cnt < 10 and i[1] < 40:
            most_alike.append([new_df.iloc[i[0]].short_name, new_df.iloc[i[0]].club_name,
                              new_df.iloc[i[0]].nationality_name, new_df.iloc[i[0]].player_positions, str(new_df.iloc[i[0]].overall)])
            a_cnt += 1

    for i in player_list:
        if new_df.iloc[i[0]].value_eur > 70000000 and e_cnt < 5 and i[1] < 40:
            expensive.append([new_df.iloc[i[0]].short_name, new_df.iloc[i[0]].club_name,
                             new_df.iloc[i[0]].nationality_name, new_df.iloc[i[0]].player_positions, str(new_df.iloc[i[0]].overall)])
            e_cnt += 1
        elif new_df.iloc[i[0]].value_eur <= 30000000 and c_cnt < 5 and i[1] < 40:
            cheap.append([new_df.iloc[i[0]].short_name, new_df.iloc[i[0]].club_name,
                         new_df.iloc[i[0]].nationality_name, new_df.iloc[i[0]].player_positions, str(new_df.iloc[i[0]].overall)])
            c_cnt += 1
        elif m_cnt < 5 and i[1] < 40:
            medium.append([new_df.iloc[i[0]].short_name, new_df.iloc[i[0]].club_name,
                          new_df.iloc[i[0]].nationality_name, new_df.iloc[i[0]].player_positions, str(new_df.iloc[i[0]].overall)])
            m_cnt += 1
    return most_alike, expensive, medium, cheap


def find_by_stat(p, s, ps, dr, d, ph, di, h, k, po, r, selected_position):
    distances = []
    curr_df = new_df
    if selected_position == 'Goalkeeper':
        curr_df = new_df[new_df['player_positions'] == 'GK']
    elif selected_position == 'Forward':
        curr_df = new_df[new_df['player_positions'].isin(['LW', 'RW', 'ST', 'CF'])]
    elif selected_position == 'Midfielder':
        curr_df = new_df[new_df['player_positions'].isin(['CAM', 'CDM', 'CM', 'LM', 'RM'])]
    else:
        curr_df = new_df[new_df['player_positions'].isin(['CB', 'LB', 'RB', 'LWB', 'RWB'])]

    for index, row in curr_df.iterrows():
        distance = euclidean([p, s, ps, dr, d, ph, di, h, k, po, r], [
            row['pace'], row['shooting'], row['passing'], row['dribbling'], row['defending'], row['physic'], row['goalkeeping_diving'], row['goalkeeping_handling'], row['goalkeeping_kicking'], row['goalkeeping_positioning'], row['goalkeeping_reflexes']])
        distances.append(distance)
        player_list = sorted(list(enumerate(distances)), key=lambda x: x[1])

    most_alike = []
    a_cnt = 0

    for i in player_list:
        if a_cnt < 10 and i[1] < 75:
            most_alike.append([curr_df.iloc[i[0]].short_name, curr_df.iloc[i[0]].club_name,
                              curr_df.iloc[i[0]].nationality_name, curr_df.iloc[i[0]].player_positions, str(curr_df.iloc[i[0]].overall)])
            a_cnt += 1
    return most_alike


def player_info(player):
    player_index = new_df[new_df['short_name'] == player].index[0]
    L = []
    L.append(new_df.iloc[player_index].short_name)
    L.append(new_df.iloc[player_index].player_positions)
    L.append(new_df.iloc[player_index].club_name)
    L.append(new_df.iloc[player_index].nationality_name)
    L.append(new_df.iloc[player_index].value_eur)
    L.append(new_df.iloc[player_index].overall)
    L.append(new_df.iloc[player_index].overall_percentile)
    L.append(new_df.iloc[player_index].pace)
    L.append(new_df.iloc[player_index].pace_percentile)
    L.append(new_df.iloc[player_index].shooting)
    L.append(new_df.iloc[player_index].shooting_percentile)
    L.append(new_df.iloc[player_index].passing)
    L.append(new_df.iloc[player_index].passing_percentile)
    L.append(new_df.iloc[player_index].dribbling)
    L.append(new_df.iloc[player_index].dribbling_percentile)
    L.append(new_df.iloc[player_index].defending)
    L.append(new_df.iloc[player_index].defending_percentile)
    L.append(new_df.iloc[player_index].physic)
    L.append(new_df.iloc[player_index].physic_percentile)
    L.append(new_df.iloc[player_index].goalkeeping_diving)
    L.append(new_df.iloc[player_index].goalkeeping_diving_percentile)
    L.append(new_df.iloc[player_index].goalkeeping_handling)
    L.append(new_df.iloc[player_index].goalkeeping_handling_percentile)
    L.append(new_df.iloc[player_index].goalkeeping_kicking)
    L.append(new_df.iloc[player_index].goalkeeping_kicking_percentile)
    L.append(new_df.iloc[player_index].goalkeeping_positioning)
    L.append(new_df.iloc[player_index].goalkeeping_positioning_percentile)
    L.append(new_df.iloc[player_index].goalkeeping_reflexes)
    L.append(new_df.iloc[player_index].goalkeeping_reflexes_percentile)

    return L


st.set_page_config(page_title="Fifa Career Mode Guide")


custom_css = """
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(to bottom left, #5D79BA 40%, #FED5C9);
    color:#000;
}
[data-testid="baseButton-secondary"] {
    color:#ff4b4b;
}
[data-testid="stThumbValue"] {
    color:#fff;
}
</style>
"""


# linear-gradient(to right, #87CEFA, #800080)
# url(https://images.pexels.com/photos/7130473/pexels-photo-7130473.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1)

st.title('FIFA 22 CAREER MODE GUIDE')


st.markdown(custom_css, unsafe_allow_html=True)


st.markdown("<hr>", unsafe_allow_html=True)
st.write(f"<p style='font-size:35px;'>Top 10 players by overall:</p>",
         unsafe_allow_html=True)
selected_attributes = ['short_name', 'club_name',
                       'nationality_name', 'player_positions', 'overall']
for index, row in new_df[selected_attributes].head(10).iterrows():
    row_string = ' | '.join(
        [f"{row[attribute]}" for attribute in selected_attributes])
    st.text(row_string)


st.markdown("<hr>", unsafe_allow_html=True)
st.write(f"<p style='font-size:35px;'>Filter Players:</p>",
         unsafe_allow_html=True)

positions_sorted = sorted(new_df['player_positions'].unique())
positions_sorted.insert(0, 'All')
selected_position = st.selectbox(
    'Filter Position:', positions_sorted)

clubs_sorted = sorted(new_df['club_name'].unique())
clubs_sorted.insert(0, 'All')
selected_club = st.selectbox('Filter Club:', clubs_sorted)

nations_sorted = sorted(new_df['nationality_name'].unique())
nations_sorted.insert(0, 'All')
selected_nation = st.selectbox('Filter Nation:', nations_sorted)

ovr_min_threshold = st.slider(
    'Minimum Overall:', min_value=77, max_value=93, value=77)

ovr_max_threshold = st.slider(
    'Maximum Overall:', min_value=77, max_value=93, value=93)

value_min_threshold = st.slider(
    'Minimum Value(in Million):', min_value=0, max_value=194, value=0)

value_max_threshold = st.slider(
    'Maximum Value(in Million):', min_value=0, max_value=194, value=194)

if selected_position != 'All':
    filtered_df = new_df[new_df['player_positions'] == selected_position]
else:
    filtered_df = new_df

if selected_club != 'All':
    filtered_df = filtered_df[new_df['club_name'] == selected_club]
else:
    filtered_df = filtered_df

if selected_nation != 'All':
    filtered_df = filtered_df[new_df['nationality_name'] == selected_nation]
else:
    filtered_df = filtered_df

filtered_df = filtered_df[filtered_df['overall'] >= ovr_min_threshold]
filtered_df = filtered_df[filtered_df['overall'] <= ovr_max_threshold]
filtered_df = filtered_df[filtered_df['value_eur'] >= value_min_threshold*1e6]
filtered_df = filtered_df[filtered_df['value_eur'] <= value_max_threshold*1e6]

if st.button('Find'):
    if filtered_df.empty:
        st.text("No Results. Please adjust the filter.")
    else:
        selected_attributes = ['short_name', 'club_name',
                            'nationality_name', 'player_positions', 'overall']
        for index, row in filtered_df[selected_attributes].iterrows():
            row_string = ' | '.join(
                [f"{row[attribute]}" for attribute in selected_attributes])
            st.text(row_string)


st.markdown("<hr>", unsafe_allow_html=True)
st.write(f"<p style='font-size:35px;'>Search Players by Name:</p>",
         unsafe_allow_html=True)

selected_player = st.selectbox(
    'Enter Player Name:',
    new_df['short_name'].values
)

if st.button('Search'):
    L = player_info(selected_player)
    st.write(f"<p style='font-size:45px;'>{L[0]}</p>",
             unsafe_allow_html=True)
    st.write(f"<p style='font-size:25px;'>Club: {L[2]}</p>",
             unsafe_allow_html=True)
    st.write(f"<p style='font-size:25px;'>Nation: {L[3]}</p>",
             unsafe_allow_html=True)
    st.write(f"<p style='font-size:25px;'>Position: {L[1]}</p>",
             unsafe_allow_html=True)
    st.write(f"<p style='font-size:25px;'>Value: {L[4]} €</p>",
             unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    st.write(f"<p style='font-size:35px;'>Stats:</p>",
             unsafe_allow_html=True)
    st.write(f"<p style='font-size:25px;'>Overall: {L[5]} (Better than {L[6]}%ile)</p>",
             unsafe_allow_html=True)

    if L[1] != "GK":
        st.write(f"<p style='font-size:25px;'>Pace: {L[7]} (Better than {L[8]}%ile)</p>",
                 unsafe_allow_html=True)
        st.write(f"<p style='font-size:25px;'>Shooting: {L[9]} (Better than {L[10]}%ile)</p>",
                 unsafe_allow_html=True)
        st.write(f"<p style='font-size:25px;'>Passing: {L[11]} (Better than {L[12]}%ile)</p>",
                 unsafe_allow_html=True)
        st.write(f"<p style='font-size:25px;'>Dribbling: {L[13]} (Better than {L[14]}%ile)</p>",
                 unsafe_allow_html=True)
        st.write(f"<p style='font-size:25px;'>Defending: {L[15]} (Better than {L[16]}%ile)</p>",
                 unsafe_allow_html=True)
        st.write(f"<p style='font-size:25px;'>Physic: {L[17]} (Better than {L[18]}%ile)</p>",
                 unsafe_allow_html=True)

    else:
        st.write(f"<p style='font-size:25px;'>Diving: {L[19]} (Better than {L[20]}%ile)</p>",
                 unsafe_allow_html=True)
        st.write(f"<p style='font-size:25px;'>Handling: {L[21]} (Better than {L[22]}%ile)</p>",
                 unsafe_allow_html=True)
        st.write(f"<p style='font-size:25px;'>Kicking: {L[23]} (Better than {L[24]}%ile)</p>",
                 unsafe_allow_html=True)
        st.write(f"<p style='font-size:25px;'>Positioning: {L[25]} (Better than {L[26]}%ile)</p>",
                 unsafe_allow_html=True)
        st.write(f"<p style='font-size:25px;'>Reflexes: {L[27]} (Better than {L[28]}%ile)</p>",
                 unsafe_allow_html=True)

    list1, list2, list3, list4 = recommend(selected_player)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.write("<p style='font-size:25px;'>Players having similar stats:</p>",
             unsafe_allow_html=True)
    for i in list1:
        st.text(" | ".join(i))

    st.markdown("<hr>", unsafe_allow_html=True)
    st.write("<p style='font-size:25px;'>High Budget Alternatives (>70M):</p>",
             unsafe_allow_html=True)
    for i in list2:
        st.text(" | ".join(i))

    st.markdown("<hr>", unsafe_allow_html=True)
    st.write("<p style='font-size:25px;'>Medium Budget Alternatives (<=70M & >30M):</p>",
             unsafe_allow_html=True)
    for i in list3:
        st.text(" | ".join(i))

    st.markdown("<hr>", unsafe_allow_html=True)
    st.write("<p style='font-size:25px;'>Low Budget Alternatives (<=30M):</p>",
             unsafe_allow_html=True)
    for i in list4:
        st.text(" | ".join(i))


st.markdown("<hr>", unsafe_allow_html=True)
st.write(f"<p style='font-size:35px;'>Search Players by Stats:</p>",
         unsafe_allow_html=True)

selected_position = st.selectbox(
    'Enter Player Position:',
    ('Goalkeeper', 'Defender', 'Midfielder', 'Forward')
)

p, s, ps, dr, d, ph, di, h, k, po, r = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

if selected_position == 'Goalkeeper':
    di = st.slider('Diving:', min_value=73, max_value=91, value=82)
    h = st.slider('Handling:', min_value=70, max_value=92, value=81)
    k = st.slider('Kicking:', min_value=60, max_value=93, value=76)
    po = st.slider('Positioning:', min_value=71, max_value=92, value=81)
    r = st.slider('Reflexes:', min_value=75, max_value=90, value=82)
elif selected_position == 'Defender':
    p = st.slider('Pace:', min_value=32, max_value=96, value=64)
    s = st.slider('Shooting:', min_value=22, max_value=77, value=49)
    ps = st.slider('Passing:', min_value=44, max_value=88, value=66)
    dr = st.slider('Dribbling:', min_value=49, max_value=88, value=68)
    d = st.slider('Defending:', min_value=70, max_value=91, value=80)
    ph = st.slider('Physic:', min_value=58, max_value=89, value=73)
elif selected_position == 'Midfielder':
    p = st.slider('Pace:', min_value=33, max_value=88, value=60)
    s = st.slider('Shooting:', min_value=42, max_value=86, value=64)
    ps = st.slider('Passing:', min_value=62, max_value=93, value=77)
    dr = st.slider('Dribbling:', min_value=65, max_value=91, value=78)
    d = st.slider('Defending:', min_value=24, max_value=87, value=55)
    ph = st.slider('Physic:', min_value=42, max_value=90, value=66)
else:
    p = st.slider('Pace:', min_value=36, max_value=97, value=66)
    s = st.slider('Shooting:', min_value=64, max_value=94, value=79)
    ps = st.slider('Passing:', min_value=48, max_value=91, value=69)
    dr = st.slider('Dribbling:', min_value=65, max_value=95, value=80)
    d = st.slider('Defending:', min_value=20, max_value=76, value=48)
    ph = st.slider('Physic:', min_value=45, max_value=88, value=66)


if st.button('Enter'):
    similar_players = find_by_stat(
        p, s, ps, dr, d, ph, di, h, k, po, r, selected_position)

    st.write("<p style='font-size:25px;'>Players having similar stats:</p>",
             unsafe_allow_html=True)
    for player in similar_players:
        st.text(" | ".join(player))

st.markdown("<hr>", unsafe_allow_html=True)

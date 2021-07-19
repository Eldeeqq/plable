from numpy.random.mtrand import weibull
from plable.components import overlap
from oauthlib.oauth2.rfc6749.clients import base
import streamlit as st


from plable.handler import get_parallels, kosapy
from plable.solver import solve
from plable.fitness import overlap_fitness
from plable.renderer import render
from plable.solver import decode


st.set_page_config(page_title='Class planner | FIT CTU', layout = 'wide', initial_sidebar_state = 'auto')
st.sidebar.title('Class planner for FIT CTU')


subjects = []
info = None
plans = []

text = st.sidebar.text_area('Enter course codes (e. g. BI-PA1) separated with newlines')
semester = st.sidebar.selectbox("Semester", ['current']+[f'B{y}{s}' for y in range(17, 25) for s in [1, 2] ])
option = st.sidebar.selectbox("Criterion", options=["Minimize collisions"])

choice = st.empty()

if st.sidebar.button("Generate", key='g'):

    if subjects or text.strip() != '':
        subjects = set(text.split('\n'))
        if subjects:
            with st.spinner(text='Trying combinations...'):
                print(semester)
                parallels, counters = get_parallels(subjects, semester=semester)
                plans = solve(parallels, counters, fitness=lambda x: overlap_fitness(x, parallels), weights=(-1,)).items
                if plans:
                    st.session_state['PLANS'] = plans
                    st.session_state['PARALLELS'] = parallels
    else:
        st.image("pepe.gif")
        st.text("You have to input courses and stuff 🤡")

if 'PLANS' in st.session_state:
    if not st.session_state['PLANS'] or st.session_state['PLANS'][0] == [] :
        st.image("cat.gif")
        st.text("No solution found 😿")
    
    else:
        choice = choice.slider("Preview parallel", min_value=0, max_value=len(st.session_state['PLANS'])-1)
        decoded = decode(st.session_state['PLANS'][choice],st.session_state['PARALLELS'])
        base64_pdf = render(decoded)
            # time.sleep(3)
        pdf_2_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="90%" height="800" type="application/pdf">'
        st.markdown(pdf_2_display, unsafe_allow_html=True)
        
        for x in decoded:
            st.sidebar.text(f'{x}')
        


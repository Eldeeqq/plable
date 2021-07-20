import re
from numpy.random.mtrand import weibull
from plable.components import overlap
from oauthlib.oauth2.rfc6749.clients import base
import streamlit as st


from plable.handler import get_parallels, get_class_paralles
from plable.solver import solve
from plable.fitness import overlap_fitness
from plable.renderer import render
from plable.solver import decode

st.set_page_config(page_title="Class planner | FIT CTU", layout="wide", initial_sidebar_state="auto")


padding = 0
st.markdown(
    f""" <style>
    .reportview-container .main .block-container{{
        padding-top: {padding}rem;
        padding-bottom: {padding}rem;
    }} </style> """,
    unsafe_allow_html=True,
)

st.markdown(
    """ <style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style> """,
    unsafe_allow_html=True,
)

st.sidebar.title("Class planner for FIT CTU")

subjects = []
info = None
plans = []

text = st.sidebar.text_area("Enter course codes (e. g. BI-PA1) separated with commas")
semester = st.sidebar.selectbox(
    "Semester",
    ["current", "next"] + [f"B{y}{s}" for y in range(17, 25) for s in [1, 2]],
)
option = st.sidebar.selectbox("Criterion", options=["Minimal collisions"])

choice = st.empty()

if "CLICKED" not in st.session_state:
    st.session_state["CLICKED"] = False
if "DONE" not in st.session_state:
    st.session_state["DONE"] = False
if "ID" not in st.session_state:
    st.session_state["ID"] = 0


if st.sidebar.button("Generate", key="g"):
    st.session_state["CLICKED"] = True
    st.session_state["DONE"] = False
    st.session_state["PLANS"] = None
    st.session_state["PARALLELS"] = None
    st.session_state["ID"] = 0

    subjects = set(filter(lambda x: x, re.sub("\s", "", text).split(",")))

    if subjects:
        parallels, counters = {}, {}
        # try load parallels
        for subject in subjects:
            _parallels, _counters = get_class_paralles(subject, semester)
            if not _parallels:
                st.warning(f"Could not load {subject}")
            else:
                parallels.update({subject: _parallels})
                counters.update({subject: _counters})
        # try solve timetable
        if parallels:
            with st.spinner(text="Trying combinations..."):
                plans = solve(
                    parallels,
                    counters,
                    fitness=lambda x: overlap_fitness(x, parallels),
                    weights=(-1,),
                ).items
                if plans:
                    st.session_state["PLANS"] = plans
                    st.session_state["PARALLELS"] = parallels
                st.session_state["DONE"] = True


if st.session_state["CLICKED"] and not st.session_state["DONE"]:
    st.image("img/wrong.gif")
    st.text("Something went wrong 😔")

if st.session_state["CLICKED"] and st.session_state["PLANS"]:
    plan_len = len(st.session_state["PLANS"])
    if plan_len == 0:
        st.image("img/cat.gif")
        st.text("No solution found 😿")
    else:
        col1, _, col2, _, col3 = st.beta_columns(5)
        if col1.button("<"):
            if st.session_state["ID"] > 0:
                st.session_state["ID"] -= 1

        if col3.button(">"):
            if st.session_state["ID"] < plan_len - 1:
                st.session_state["ID"] += 1

        if plan_len >= 1:
            col2.text(f"{st.session_state['ID']+1}/{plan_len}")

        choice = st.session_state["ID"]
        decoded = decode(st.session_state["PLANS"][choice], st.session_state["PARALLELS"])
        base64_pdf = render(decoded)
        # time.sleep(3)
        pdf_2_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="83%" height="800" type="application/pdf">'
        st.markdown(pdf_2_display, unsafe_allow_html=True)

        st.sidebar.text("Planned timetable:")
        st.sidebar.text("\n".join([str(x) for x in decoded]))

if not st.session_state["CLICKED"]:
    print("hello")
    with open("README.md", "r") as f:
        md = f.read()
    st.markdown(md, unsafe_allow_html=True)

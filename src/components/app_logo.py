import os

import streamlit as st


def show_app_logo():
    return st.logo(
        image=os.getcwd() + "/asserts/lng2p_fm_logo.png",
        icon_image=None,
        size="large",
    )

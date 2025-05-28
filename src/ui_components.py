import streamlit as st

from meta import __version__


# region Components
def add_version_info():
    import platform
    import sys
    lib_version:str = __version__
    python_version_platform = platform.python_version()
    python_version_sys = sys.version
    add_bottom_right_footer_text(f"v{lib_version} on {python_version_platform}", python_version_sys)
# endregion

# region Layout Helpers
def add_bottom_right_footer_text(text:str, tooltip:str = None):
    """
    Adds text at the bottom-right
    :param text:
    :param tooltip:
    :return:
    """
    st.markdown(
        f"""
        <style>
        .version-info {{
            position: fixed;
            bottom: 10px;
            right: 10px;
            font-size: 12px;
            color: gray;
        }}
        </style>
        <div class="version-info" title='{tooltip}'>
            {text}
        </div>
        """,
        unsafe_allow_html=True
    )
# endregion

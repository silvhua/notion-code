import solara
import sys
sys.path.append(r"/home/silvhua/repositories/notion/src")
from components.invoice import *
@solara.component
def Layout(children):
    return solara.AppLayout(
        navigation=False, children=children,
        sidebar_open=False
        )
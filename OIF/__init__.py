import solara
@solara.component
def Layout(children):
    
    return solara.AppLayout(navigation=False, children=children)
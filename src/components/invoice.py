import sys
sys.path.append(r"/home/silvhua/repositories/notion/src")
sys.path.append(r"/home/silvhua/custom_python")
import solara
from silvhua import load_txt

address_filepath = '/home/silvhua/repositories/notion/private'
@solara.component
def Load_Text(filename, path):
    text = load_txt(filename, path)
    text = text.replace('\n', '\n\n')
    return solara.Markdown(text)

@solara.component
def Invoice_Header(client: str):
    solara.Title('hello')
    with solara.Columns([1,1]):
        solara.Markdown('BILL TO:')
        solara.Markdown('FROM:')
    with solara.Columns([1,1]):
        Load_Text(f'{client}_address.txt', address_filepath)
        Load_Text('address.txt', address_filepath)
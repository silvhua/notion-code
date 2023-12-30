import sys
sys.path.append(r"/home/silvhua/repositories/notion/src")
from notion_functions import *
from data_viz import *
from silvhua import *

print('start of Python script')

def main():
    # Access filenames from command line arguments
    if len(sys.argv) > 1:
        filename = sys.argv[1:][0]
        print("File name:", filename)
        
        path = '/home/silvhua/repositories/notion/data/'
        df = create_notion_df(filename, path)
        notion_filename = 'notion_df'
        savepickle(
            df, notion_filename, path=path, append_version=False,
        )
        update_df_attributes(
            df, df_filename=notion_filename, json_filename='df_attributes',
            path='/home/silvhua/repositories/notion/data'
            )


if __name__ == "__main__":
    main()

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
        attributes_filename = sys.argv[1:][1] if len(sys.argv) > 2 else 'df_attributes'
        notion_filename = sys.argv[1:][2] if len(sys.argv) > 3 else 'notion_df'
        print("File name:", filename)
        
        path = '/home/silvhua/repositories/notion/data/'
        df = create_notion_df(filename, path)
        savepickle(
            df, notion_filename, path=path, append_version=False,
        )
        update_df_attributes(
            df, df_filename=notion_filename, json_filename=attributes_filename,
            path='/home/silvhua/repositories/notion/data'
            )


if __name__ == "__main__":
    main()

import os
import sys
sys.path.append(r"/home/silvhua/repositories/notion/src")
from notion_functions import *
from data_viz import *
from silvhua import *

print('start of Python script')

def main():
    print(f'Number of system arguments: {len(sys.argv)}')
    # Access filenames from command line arguments
    if len(sys.argv) > 1:
        json_filename = f'{sys.argv[1]}.json'
        notion_filename = sys.argv[2] if len(sys.argv) > 2 else 'notion_df'
        attributes_filename = 'df_attributes'
        print(f'Parsed JSON filename: {json_filename}')
        print(f'Notion DataFrame filename: {notion_filename}')
        print(f'DataFrame attributes filename: {attributes_filename}')

        path = '/home/silvhua/repositories/notion/data/'
        # check if f'{notion_filename}.sav' exists in the `path`
        if f'{notion_filename}.sav' not in os.listdir(path):
            print(f'** {notion_filename}.sav does not exist in {path}. Creating blank DataFrame.')
            original_df = pd.DataFrame()
        else:
            original_df = loadpickle(
                f'{notion_filename}.sav', path
            )
        new_df = create_notion_df(
            json_filename, filepath='.',
            # split_columns=['Task Name', 'Task Project tags']
            )
        print(f'New Rows DataFrame shape: {new_df.shape}')

        df = pd.concat([original_df, new_df])
        print(f'DataFrame shape after concatenation and before duplicate removal: {df.shape}')
        df = df.sort_values(by=['created_time'])
        df = df.reset_index(drop=True)
        df = df.drop_duplicates(subset=['id', 'created_time']) 
        print(f'\nFinal updated DataFrame shape: {df.shape}\n')
        savepickle(
            df, notion_filename, path=path, append_version=False,
        )
        update_df_attributes(
            df, df_filename=f'{notion_filename}.sav', json_filename=attributes_filename,
            path=path
            )
        print('end of Python script')
    else:
        print('Please provide a JSON filename as an argument.')


if __name__ == "__main__":
    main()

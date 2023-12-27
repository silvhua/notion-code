import sys
sys.path.append(r"/home/silvhua/custom_python")
from silvhua import *
from wrangling import filter_df_all_conditions

def create_notion_df(
    filename, filepath, split_columns=['Task Name', 'Task Project name']
    ):
    data = load_json(filename, filepath)
    df = pd.DataFrame(data).transpose()
    for split_column in split_columns:
        # Explode the rows based on the values in the split_column
        df = df.explode(split_column)
    
    columns = df.columns.tolist()
    columns.remove('url')
    columns.remove('Name')
    columns.remove('Task Project')
    df.index.name = 'id'
    columns = ['Name'] + columns + ['url', 'id']
    df = df.reset_index()
    df = df[columns]
    df = df.drop_duplicates(subset=['id', 'Task Project name', 'Task Name']) 
    print(f'Shape before applying filter: {df.shape}')
    filters = {
        'Elapsed': '> 0'
    }
    df['created_time'] = pd.to_datetime(df['created_time']).dt.tz_convert('America/Vancouver')

    return filter_df_all_conditions(df, filters)  

def notion_df(filename, filepath):

    def parse_property(property_dict, property):
        value = None
        # print(property_dict.keys())
        property_type = property_dict['type']
        if property_type in columns_to_ignore:
            value = None
        elif property_type == 'rollup':
            rollup_type = property_dict[property_type]['type']
            # print(f'\t{rollup_type}')
            if (rollup_type == 'array') & (len(property_dict[property_type][rollup_type]) > 0):
                array_type = property_dict[property_type][rollup_type][0]['type']
                # print(f'\t\t{array_type}')
                if array_type in ['multi_select', 'relation']:
                    value = []
                    for item in property_dict[property_type][rollup_type]:
                        value.append(item[array_type][0]['name'] if len(item[array_type]) > 0 else None)
        elif property_type == 'rich_text':
            if len(property_dict[property_type]) > 0:
                value = property_dict[property_type][0]['text']['content']
        elif property_type == 'multi_select': 
            if len(property_dict[property_type]) > 0:
                value = property_dict[property_type]
        elif property_type == 'formula':
            formula_type = property_dict[property_type]['type']
            value = property_dict[property_type][formula_type]
        elif property_type == 'relation':
            if len(property_dict[property_type]) > 0:
                value = []
                for item in property_dict[property_type]:
                    value.append(item['id'])
                # value = value[0]
        else:
            print(property, property_type)
            # print(property_dict.keys())
            pass
        return value
            
    data = load_json(filename, filepath)
    rows = []
    metadata_columns = ['id', 'created_time', 'url']
    columns_to_ignore = [
            'Created time', 'Start min', 'summary', 'End min', 'follow up task', 'URL', 'End hr', 
            'Start hr', 'Name', 'Projects', 'Project tag', 'Project (Rollup)'
        ]
    for record in data:
        row = dict()
        for column in metadata_columns:
            row[column] = record.get(column)
        for property in record['properties']:
            # print(property)
            if property not in columns_to_ignore:
                row[property] = parse_property(record['properties'][property], property)
        rows.append(pd.Series(row))
    df = pd.DataFrame(rows)
    return df

def get_unique_array_items(df, column):
    unique_values = list(set([task for tasks in df[column].values for task in tasks]))
    print(f'Unique tasks: {len(unique_values)}')
    for task in unique_values:
        print(task)
    return unique_values
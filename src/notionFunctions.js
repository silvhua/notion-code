const {getCurrentTimestamp, loadJsonFile, saveResponseJson} = require('./fileFunctions')
const { Client } = require('@notionhq/client');
const fs = require('fs');

console.log(`Current time stamp: ${getCurrentTimestamp()}`);

/**
 * Queries Notion and saves the response as a JSON file.
 *
 * @param {string} period - The period to filter the query by. Default is 'week'.
 * @param {string} jsonFileName - The name of the JSON file to save the response to. Default is '../data/notion_time_tracking'.
 * @param {boolean} save - Indicates whether to save the response as a JSON file. Default is true.
 * @param {boolean} appendTimestamp - Indicates whether to append a timestamp to the JSON file name. Default is true.
 * @return {Promise<object>} The response from the Notion API.
 */
async function queryNotionAndSaveResponse(
  period='week', jsonFileName='../data/notion_time_tracking', save = true, appendTimestamp = true) {
  let notionApiKey = process.env.notion_secret;
  let notion = new Client({ auth: notionApiKey });

  if (period == 'past_week') {
    date_filter = {
      and: [
        {property: 'Elapsed', number: {greater_than: 0}},
        {property: 'Created time', date: {past_week: {}}},
        {property: 'Tasks', relation: {is_not_empty: true}}
      ]
    };
  } else if (period == 'quarter') {
    let start = getTimestamp('month', nMonths = 3);
    console.log(`Start date: ${start}. Period: ${period}`);
    date_filter = {
      and: [
        {property: 'Created time', date: {on_or_after: start}},
        {property: 'Created time', date: {before: addTimeDelta(start, period='month', nPeriod=3)}},
        {property: 'Elapsed', number: {greater_than: 0}},
        {property: 'Tasks', relation: {is_not_empty: true}}
      ]
    };
  } else if (period == 'month' || period == 'week') {
      start = getTimestamp(period)
      date_filter = {
        and: [
          {property: 'Created time', date: {on_or_after: start}},
          {property: 'Created time', date: {before: addTimeDelta(start, period=period, nPeriod=1)}},
          {property: 'Elapsed', number: {greater_than: 0}},
          {property: 'Tasks', relation: {is_not_empty: true}}
        ]
      };
  };
  const pages = [];
  let cursor = undefined;
  while (true) {
    const {results, next_cursor} = await notion.databases.query({
      database_id: process.env.notion_database,
      filter: date_filter,
      start_cursor: cursor
    });
    pages.push(...results);
    if (!next_cursor) {
      break
    };
    cursor = next_cursor
  }
  await console.log(`${pages.length} issues successfully fetched.`)


  if (save) {
    let fileName = jsonFileName;
    // Add timestamp to the file name if appendTimestamp is true
    if (appendTimestamp) {
      const timestamp = getCurrentTimestamp();
      fileName = `${jsonFileName}_${timestamp}`;
    }

    // Save the response as a JSON file
    await fs.promises.writeFile(`${fileName}.json`, JSON.stringify(pages, null, 2));
    
    console.log(`Response saved to ${fileName}.json`);
  }
  return pages
}

/**
 * Converts a given date string to an ISO timestamp.
 *
 * @param {string} dateString - The date string to convert.
 * @return {string} The converted ISO timestamp.
 */
function getIsoTimestamp(dateString) {
    const date = new Date(dateString);
    const timestamp = date.toISOString();
    return timestamp;
  }

/**
 * Returns a timestamp based on the given option.
 *
 * @param {string} option - The option to determine the timestamp. Possible values are 'week', 'lastWeek', 'month', 'months'.
 * @param {number} [nMonths=1] - The number of months to go back if the option is 'months'.
 * @return {string|null} - The timestamp in ISO string format if the option is valid, otherwise null.
 */
function getTimestamp(option, nMonths = 1) {
  const now = new Date();

  if (option == 'week') {
    const dayOfWeek = now.getDay();
    const daysSinceLastMonday = (dayOfWeek + 6) % 7;
    const startOfLastMonday = new Date(now.getFullYear(), now.getMonth(), now.getDate() - daysSinceLastMonday);
    return startOfLastMonday.toISOString();
  }

  if (option == 'lastWeek') {
    const mondayOfLastWeek = new Date(now.getFullYear(), now.getMonth(), now.getDate() - 7 - ((now.getDay() + 6) % 7));
    return mondayOfLastWeek.toISOString();
  }

  if (option == 'month') {
    const startOfNMonthsAgo = new Date(now.getFullYear(), now.getMonth() - nMonths, 1);
    return startOfNMonthsAgo.toISOString();
  }
}

/**
 * Adds a time delta to a given timestamp and returns the updated timestamp.
 *
 * @param {string} timestamp - The timestamp to which the time delta should be added. Defaults to the current timestamp.
 * @param {string} period - The period of the time delta. Can be 'day', 'week', or 'month'. Defaults to 'week'.
 * @param {number} nPeriod - The number of periods to add to the timestamp. Defaults to 1.
 * @return {string} - The updated timestamp in ISO 8601 format.
 */
function addTimeDelta(timestamp=new Date().toISOString(), period='week', nPeriod=1) {
  const date = new Date(timestamp);

  if (period === 'day') {
    date.setDate(date.getDate() + nPeriod);
  } else if (period === 'week') {
    date.setDate(date.getDate() + nPeriod * 7);
  } else if (period === 'month') {
    date.setMonth(date.getMonth() + nPeriod);
  }

  return date.toISOString();
}

/**
 * Retrieves a page from Notion using the page ID and returns the response.
 *
 * @param {string} pageId - The ID of the page to retrieve.
 * @param {string} jsonFileName - The name of the JSON file to save the response to. Defaults to '../data/notion_page'.
 * @param {boolean} save - Indicates whether to save the response to a JSON file. Defaults to false.
 * @param {boolean} appendTimestamp - Indicates whether to append a timestamp to the JSON file name. Defaults to true.
 * @return {Promise<Object>} The response object from Notion.
 */
async function retrievePage(
    pageId, jsonFileName='../data/notion_page', save = false, appendTimestamp = true
  ) {
    const { Client } = require('@notionhq/client');
    const fs = require('fs');
    let notionApiKey = process.env.notion_secret;
    let notion = new Client({ auth: notionApiKey });
      try {
        const response = await notion.pages.retrieve({ page_id: pageId });
        if (save) {
          await saveResponseJson(response, jsonFileName, appendTimestamp);
        }
        return response;
      } catch (error) {
        console.error(error);
        throw error;
      }
  }

  /**
   * Parses a page and retrieves specific data from it.
   *
   * @param {string} pageId - The ID of the page to parse.
   * @param {string} [database='tasks'] - The name of the database to retrieve the data from.
   * @return {object} - The parsed data from the page.
   */
  async function parsePage(pageId, database='tasks') {
    let multi_select_rollups = [];
    let relations = [];
    try {
        const data = await retrievePage(pageId);
        const parsed_data = {};
        if (database === 'tasks') {
            parsed_data['Name'] = data['properties']['Name']['title'][0]['plain_text'];
            multi_select_rollups = [
                'Project tags', 
            ]
            relations = ['Project', 'Parent-task', 'Sub-tasks'];
        } else if (database === 'projects') {
          
          parsed_data['Name'] = data['properties']['Project name']['title'][0]['plain_text'];
          multi_select_rollups = [];
          relations = [];
        } 
        if (multi_select_rollups.length > 0) {
            for (let i = 0; i < multi_select_rollups.length; i++) {
                const rollup = multi_select_rollups[i];
                parsed_data[rollup] = data['properties'][rollup]['rollup']['array'][0]['multi_select'].map(item => item['name']);
            }            
        }
        if (relations.length > 0) {
            for (let i = 0; i < relations.length; i++) {
                const relation = relations[i];
                //  Only parse relation if it is greater than 0
                if (data['properties'][relation]['relation'].length === 0) {
                    parsed_data[relation] = null;
                } else {
                    parsed_data[relation] = data['properties'][relation]['relation'][0]['id'];
                };
            }
        }
        return parsed_data
    } catch (error) {
        console.log(`Error for database ${database}: ${error}`);
    };
}

/**
 * Parses the time tracking data.
 *
 * @param {Array} data - The time tracking data to be parsed.
 * @param {boolean} [save=false] - Indicates whether to save the parsed data.
 * @param {string} [jsonFileName='../data/notion_time_tracking_parsed'] - The file name to save the parsed data.
 * @param {boolean} [appendTimestamp=true] - Indicates whether to append a timestamp to the file name.
 * @return {Object} - The parsed time tracking data.
 */
async function parseTimeTracking(
  data, save = false, jsonFileName='../data/notion_time_tracking_parsed', appendTimestamp = true
) {
  const parsed_data = {};
  const relations_list = ['Tasks'];
  const array_types = ['multi_select', 'relation'];
  let properties = Object.keys(data[0]['properties']);
  const to_ignore = ['Notes', 'Last edited', 'Created time', 'Start min', 'summary', 'End min', 'follow up task', 'URL', 'End hr', 'Start hr', 'Projects', 'Project tag', 'Project (Rollup)'];
  properties = properties.filter(item => !to_ignore.includes(item));
  console.log(`Parsing...`);

  // for (let i = 0; i < 3; i++) {
  for (let i = 0; i < data.length; i++) {
    try {
      const item = data[i];
      const id = item['id'];
      const record = {};
      console.log(`\trecord ${i}, id ${id}`);
      record['url'] = item['url'];
      record['created_time'] = item['created_time'];

      for (let j = 0; j < properties.length; j++) {
        const property = properties[j];
        const property_dict = data[i]['properties'][property];
        const property_type = property_dict['type'];

        if (property_type === 'relation') {
          if (property_dict[property_type].length === 0) {
            record[property] = null;
          } else {
            const relationValues = property_dict[property_type];
        
        
            if (property === 'Tasks') {
              const taskProjects = [];
              const taskProjectTags = [];
        
              for (let k = 0; k < relationValues.length; k++) {
                const task_details = await parsePage(relationValues[k]['id'], database='tasks');
                
                const attributes = Object.keys(task_details);
                const attribute_dict = {};
                for (let attribute = 0;attribute < attributes.length; attribute++) {
                  const attribute_list = [];
                  attribute_list.push(task_details[attributes[attribute]]);
                  attribute_dict[attributes[attribute]] = attribute_list;
                };
                const projectId = task_details['Project'];
                const project = await parsePage(projectId, 'projects');
                
                let project_attributes = Object.keys(project);
                // console.log(project_attributes);
                for (let c = 0; c < project_attributes.length; c++) {
                  const attribute_list = [];
                  attribute_list.push(project[project_attributes[c]]);
                  if (project_attributes[c] === 'Name') {
                    project_attributes[c] = 'Project name';
                  };
                  attribute_dict[project_attributes[c]] = attribute_list;
                };
                const task_attributes = Object.keys(attribute_dict)
                for (let c = 0; c < task_attributes.length; c++) {
                  record[`Task ${task_attributes[c]}`] = attribute_dict[task_attributes[c]]; // task attributes
                };
              }
            }
          }
        } else if (property_type === 'rollup') {
          rollup_type = property_dict[property_type]['type'];

          if (rollup_type === 'array' && property_dict[property_type]['array'].length > 0) {
            const array_type = property_dict[property_type]['array'][0]['type'];

            if (array_type === 'multi_select' || array_type === 'relation') {
              record[property] = property_dict[property_type]['array'][0][array_type].map(item => item['name']);
            } else {
              record[property] = null;
            }
          } else {
            record[property] = null;
          }
        } else if (property_type === 'rich_text' || property_type === 'title') {
          if (property_dict[property_type].length > 0) {
            record[property] = property_dict[property_type][0]['text']['content'];
          } else {
            record[property] = null;
          }
        } else if (property_type === 'formula') {
          formula_type = property_dict[property_type]['type'];
          record[property] = property_dict[property_type][formula_type];
        } else if (property_type === 'multi_select') {
          if (property_dict[property_type].length > 0) {
            record[property] = property_dict[property_type].map(item => item);
          } else {
            record[property] = null;
          }
        } else {
          console.log(`\t\tProperty of type ${property_type} was not parsed: ${property}`);
        }
      }

      parsed_data[id] = record;
    } catch (error) {
      console.error(error);
      break;
    }
  }

  if (save) {
    saveResponseJson(parsed_data, jsonFileName, appendTimestamp);
  }

  return parsed_data;
}

module.exports = {
  queryNotionAndSaveResponse,
  getIsoTimestamp,
  getTimestamp,
  addTimeDelta,
  retrievePage,
  parsePage,
  parseTimeTracking
}
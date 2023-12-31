
console.log(`\nRunning fixPageParsing.js`);
const {loadJsonFile, saveResponseJson, getCurrentTimestamp} = require('./fileFunctions');
const nf = require('./notionFunctions');
const path = require('path');
const fs = require('fs');
async function main() {
    const df_key = 'notion_df';
    console.log(`df_key: ${df_key}`)
  
    const root_path = 'data'


    let jsonFileName = `${root_path}/raw/notionTimeTracking_quarter_2023-12-27_0045`;
    const parsedJsonFileName = `${root_path}/notion_time_tracking_parsed_quarter_2023-12-27_0045`;

    // let jsonFileName = `${root_path}/raw/notionTimeTracking_quarter_2023-12-27_0045`;
    // const parsedJsonFileName = `${root_path}/notion_time_tracking_parsed_quarter_2023-12-27_0045`;

    // let jsonFileName = `${root_path}/raw/NewNotionTimeTracking_2023-12-30T17:22:00-08:00`;
    // const parsedJsonFileName = `${root_path}/NewNotionTimeTracking_parsed_2023-12-30T17:22:00-08:00_v2`;
    
    // let jsonFileName = `${root_path}/raw/NewNotionTimeTracking_2023-11-30T20:26:00-08:00`;
    // const parsedJsonFileName = `${root_path}/NewNotion_time_tracking_parsed_2023-11-30T20:26:00-08:00_v2`;

    const data = loadJsonFile(`${jsonFileName}.json`);
    const parsedData = nf.parseTimeTracking(
      data, save=true, path.resolve(parsedJsonFileName),
      appendTimestamp = false
      );
    fs.writeFileSync(`${root_path}/filename.txt`, parsedJsonFileName, 'utf-8');
    console.log(`Filename saved to ${root_path}/filenames.txt`);
  }
  
  main().catch(error => {
    console.error('Error:', error);
  });
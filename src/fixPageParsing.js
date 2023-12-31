
console.log(`\nRunning fixPageParsing.js`);
const {loadJsonFile, saveResponseJson, getCurrentTimestamp} = require('./fileFunctions');
const nf = require('./notionFunctions');
const path = require('path');
const fs = require('fs');
async function main() {
    // const newest_created_time = process.argv[2];
    // if process.argv has more than 3 elements, assign the 4th element as df_key, otherwise, df_key is 'notion_df'
    const df_key = 'notion_df';
    console.log(`df_key: ${df_key}`)
  
    // console.log(`Newest record created_time (1): ${ newest_created_time }`)
    const root_path = 'data'

    let jsonFileName = `${root_path}/raw/NewNotionTimeTracking_2023-12-30T17:22:00-08:00`;
    const parsedJsonFileName = `${root_path}/NewNotionTimeTracking_parsed_2023-12-30T17:22:00-08:00_v2`;
    
    // let jsonFileName = `${root_path}/raw/NewNotionTimeTracking_2023-11-30T20:26:00-08:00`;
    // const parsedJsonFileName = `${root_path}/NewNotion_time_tracking_parsed_2023-11-30T20:26:00-08:00_v2`;


    // const notionResponse = await nf.getNewNotionData(
    //   df_key, df_attributes_file=`${root_path}/df_attributes.json`,
    //   jsonFileName, save = true, appendTimestamp = false
    //   )
    // jsonFileName += `_${newest_created_time}`;
  
    const data = loadJsonFile(`${jsonFileName}.json`);
    // console.log(data)
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
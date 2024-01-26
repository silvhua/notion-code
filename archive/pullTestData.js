
console.log(`\nRunning fixPageParsing.js`);
const {loadJsonFile, saveResponseJson, getCurrentTimestamp} = require('../fileFunctions');
const nf = require('../notionFunctions');
const path = require('path');
const fs = require('fs');
async function main() {
    const df_key = 'notion_df_test';
    console.log(`df_key: ${df_key}`)
  
    const root_path = 'data'

    let jsonFileName = `${root_path}/raw/notionTimeTracking_test_2024-01-10_10:58`;
    const parsedJsonFileName = `${root_path}/notion_time_tracking_parsed_test_2024-01-10_10:58`;
    const notionResponse = await nf.getNewNotionData(
      df_key, df_attributes_file=`${root_path}/df_attributes.json`,
      jsonFileName, save = true, appendTimestamp = false
      )
    const data = loadJsonFile(`${jsonFileName}.json`);
    // const parsedData = nf.parseTimeTracking(
    //   data, save=true, path.resolve(parsedJsonFileName),
    //   appendTimestamp = false
    //   );
    // fs.writeFileSync(`${root_path}/filename.txt`, parsedJsonFileName, 'utf-8');
    // console.log(`Filename saved to ${root_path}/filenames.txt`);
  }
  
  main().catch(error => {
    console.error('Error:', error);
  });
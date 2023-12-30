console.log(`\nRunning pipelineGetData.js`);
const {loadJsonFile, saveResponseJson, getCurrentTimestamp} = require('./fileFunctions');
const nf = require('./notionFunctions');
const path = require('path');
const fs = require('fs');

async function main() {
  const newest_created_time = process.argv[2];
  // if process.argv has more than 3 elements, assign the 4th element as df_key, otherwise, df_key is 'notion_df'
  const df_key = process.argv.length > 3 ? process.argv[3] : 'notion_df';
  console.log(`df_key: ${df_key}`)

  console.log(`Newest record created_time (1): ${ newest_created_time }`)
  const root_path = './data'
  let jsonFileName = `${root_path}/raw/NewNotionTimeTracking`;
  const parsedJsonFileName = `${root_path}/NewNotion_time_tracking_parsed_${newest_created_time}`;
  const notionResponse = await nf.getNewNotionData(
    df_key, df_attributes_file=`${root_path}/df_attributes.json`,
    jsonFileName, save = true, appendTimestamp = false
    )
  jsonFileName += `_${newest_created_time}`;
//   const timeStamp = getCurrentTimestamp();
//   const jsonFileName = `${root_path}/raw/notionTimeTracking_${period}_${timeStamp}`;
//   const parsedJsonFileName = `${root_path}/notion_time_tracking_parsed_${period}_${timeStamp}`;

//   const response = await nf.queryNotionAndSaveResponse(
//     period, path.resolve(jsonFileName), save=true, appendTimestamp=false
//     );

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
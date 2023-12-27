console.log(`Running pipelineGetData.js`);
const {loadJsonFile, saveResponseJson, getCurrentTimestamp} = require('./fileFunctions');
const nf = require('./notionFunctions');
const path = require('path');

async function main() {
  const period = process.argv[2];
  const root_path = './data'
  const timeStamp = getCurrentTimestamp();
  const jsonFileName = `${root_path}/raw/notionTimeTracking_${period}_${timeStamp}`;
  const parsedJsonFileName = `${root_path}/notion_time_tracking_parsed_${period}_${timeStamp}`;

  const response = await nf.queryNotionAndSaveResponse(
    period, path.resolve(jsonFileName), save=true, appendTimestamp=false
    );

  const data = loadJsonFile(`${jsonFileName}.json`);
  const parsedData = nf.parseTimeTracking(
    data, save=true, path.resolve(parsedJsonFileName),
    appendTimestamp = false
    );
}

main().catch(error => {
  console.error('Error:', error);
});
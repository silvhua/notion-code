console.log(`Running pipelineGetData.js`);
const {loadJsonFile, saveResponseJson} = require('./fileFunctions');
const nf = require('./notionFunctions');
const path = require('path');

async function main() {
  const period = 'month';
  const jsonFileName = `./data/notionTimeTracking_${period}`;
  const parsedJsonFileName = `./data/notion_time_tracking_parsed_${period}`;

//   console.log(`path ${__dirname}`)
//   console.log(`path ${path.resolve(jsonFileName)}`)
  const response = await nf.queryNotionAndSaveResponse(
    period, path.resolve(jsonFileName), save=true, appendTimestamp=false
    );
  console.log('Response saved')
  const data = loadJsonFile(`${jsonFileName}.json`);
  const parsedData = nf.parseTimeTracking(data, save=true, path.resolve(parsedJsonFileName));
  console.log(`Done!`);

}

main().catch(error => {
  console.error('Error:', error);
});
console.log(`Running pipelineGetData.js`);
const {loadJsonFile, saveResponseJson} = require('./fileFunctions');
const nf = require('./notionFunctions');
const path = require('path');

async function main() {
//   const period = 'month';
//   const period = 'week';
//   const period = 'quarter';
  const period = process.argv[2];
  const root_path = './'
  const jsonFileName = `${root_path}data/notionTimeTracking_${period}`;
  const parsedJsonFileName = `${root_path}data/notion_time_tracking_parsed_${period}`;

  const response = await nf.queryNotionAndSaveResponse(
    period, path.resolve(jsonFileName), save=true, appendTimestamp=false
    );
  console.log('Response saved')
  const data = loadJsonFile(`${jsonFileName}.json`);
  const parsedData = nf.parseTimeTracking(data, save=true, path.resolve(parsedJsonFileName));
  await console.log(`Done!`);

}

main().catch(error => {
  console.error('Error:', error);
});
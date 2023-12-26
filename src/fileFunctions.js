const fs = require('fs');

function loadJsonFile(filename, path = '../private') {
  try {
    const filePath = `${path}/${filename}`;
    const jsonData = fs.readFileSync(filePath, 'utf8');
    const data = JSON.parse(jsonData);
    return data;
  } catch (error) {
    console.error('Error loading JSON file:', error);
    return null;
  }
}

/**
 * Returns the current timestamp in the format "YYYY-MM-DD_HHMM".
 *
 * @return {string} The formatted timestamp.
 */
function getCurrentTimestamp() {
  var date = new Date().toLocaleString("en-US", { timeZone: "America/Los_Angeles" });
  var dateTime = new Date(date);
  var year = dateTime.getFullYear();
  var month = String(dateTime.getMonth() + 1).padStart(2, "0");
  var day = String(dateTime.getDate()).padStart(2, "0");
  var hours = String(dateTime.getHours()).padStart(2, "0");
  var minutes = String(dateTime.getMinutes()).padStart(2, "0");
  var formattedTimestamp = year + "-" + month + "-" + day + "_" + hours + minutes;
  return formattedTimestamp;
}
async function saveResponseJson(data, jsonFileName, appendTimestamp) {
    var {getCurrentTimestamp} = require('../src/fileFunctions');
    const fs = require('fs');
    try {
        if (appendTimestamp) {
        const timestamp = getCurrentTimestamp();
        jsonFileName = `${jsonFileName}_${timestamp}`
        }
        await fs.promises.writeFile(`${jsonFileName}.json`, JSON.stringify(data, null, 2));
        console.log(`Saved response to ${jsonFileName}.json`);
    } catch (error) {
        console.error(error);
        throw error;
    }
}

module.exports = { 
  loadJsonFile, 
  getCurrentTimestamp,
  saveResponseJson
}

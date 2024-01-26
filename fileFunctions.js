const fs = require('fs');

/**
 * Loads a JSON file from the specified path and returns the parsed data.
 *
 * @param {string} filename - The name of the JSON file to load.
 * @param {string} [path='../private'] - The path to the directory containing the JSON file. Defaults to '../private'.
 * @return {object} The parsed JSON data from the file, or null if there was an error.
 */
function loadJsonFile(filename, path = '') {
  try {
    const filePath = `${path}${filename}`;
    console.log(`Loading JSON file: ${filePath}`);
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
/**
 * Saves the given data object as a JSON file.
 *
 * @param {object} data - The data object to be saved as JSON.
 * @param {string} jsonFileName - The name of the JSON file to be saved.
 * @param {boolean} appendTimestamp - Whether to append a timestamp to the file name.
 * @return {Promise<void>} - A Promise that resolves when the data is successfully saved.
 */
async function saveResponseJson(data, jsonFileName, appendTimestamp) {
    const fs = require('fs');
    try {
        if (appendTimestamp) {
          var {getCurrentTimestamp} = require('../src/fileFunctions');
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

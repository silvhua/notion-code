const {getCurrentTimestamp, loadJsonFile} = require('./fileFunctions')
const { Client } = require('@notionhq/client');
const fs = require('fs');

console.log(`Current time stamp: ${getCurrentTimestamp()}`);

async function queryNotionAndSaveResponse(
  period='week', jsonFileName='../data/notion_time_tracking', save = true, appendTimestamp = true) {
  let notionApiKey = process.env.notion_secret;
  let notion = new Client({ auth: notionApiKey });

  if (period == 'past_week') {
    date_filter = {
      property: 'Created time',
      date: {past_week: {}},
    };
  } else if (period == 'quarter') {
    let start = getTimestamp('month', nMonths = 3);
    console.log(`Start date: ${start}. Period: ${period}`);
    date_filter = {
      and: [
        {property: 'Created time', date: {on_or_after: start}},
        {property: 'Created time', date: {before: addTimeDelta(start, period='month', nPeriod=3)}}
      ]
    };
  } else if (period == 'month' || period == 'week') {
      start = getTimestamp(period)
      date_filter = {
        and: [
          {property: 'Created time', date: {on_or_after: start}},
          {property: 'Created time', date: {before: addTimeDelta(start, period=period, nPeriod=1)}}
        ]
      };
  };
  
  let response = await notion.databases.query({
    database_id: process.env.notion_database,
    filter: date_filter
  });


  if (save) {
    // Add timestamp to the file name if appendTimestamp is true
    if (appendTimestamp) {
      const timestamp = getCurrentTimestamp();
      jsonFileName = `${jsonFileName}_${timestamp}`;
    }

    // Save the response as a JSON file
    await fs.writeFile(`${jsonFileName}.json`, JSON.stringify(response, null, 2));

    console.log(`Response saved to ${jsonFileName}.json`);
  }
  return response
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

  // if (option == 'month') {
  //   const startOfPreviousMonth = new Date(now.getFullYear(), now.getMonth() - 1, 1);
  //   return startOfPreviousMonth.toISOString();
  // }

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
In a terminal run the relevant commands from the project root folder to accomplish the desired tasks:

Task | Command
--- | ---
**Run full pipeline**: Retrieve new data and save it to the DataFrame pickle file | **`source src/runPipeline.sh`**
Retrieve new data and save it as JSON files | `node src/pipelineGetData.js`
Test the Python data processing pipeline | `source src/runPyPipeline.sh`
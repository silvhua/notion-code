#!/bin/bash
# Run with the command `source src/createInvoice.sh Ginkgo `

VALUE=$1

source src/runPipeline.sh --no-open
python src/"$VALUE"/0_Home.py
solara run src/"$VALUE" --no-open
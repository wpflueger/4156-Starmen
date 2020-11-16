#!/usr/bin/env bash

cd src && gunicorn app:app

TS=$(date +%s)
FLDR="report-${TS}"

function header {
    echo "============ upmed-web $1 Report Generated on ${TS} ============"
    echo $'\n\n'
}

# Create output folder
mkdir "tst/Reports/${FLDR}"

# Linting
echo "Writing coverage and unit testing report to tst/reports/${FLDR}/coverage.txt."
echo $(header "Coverage and Unit") >> "tst/reports/${FLDR}/coverage.txt"
python3 tst
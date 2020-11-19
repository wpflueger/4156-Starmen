TS=$(date +%s)
FLDR="report-${TS}"
function header() {
    echo "============ upmed-web $1 Report Generated on ${TS} ============"
    echo '\n\n'
}
# Create output folder
mkdir "tst/Reports/${FLDR}"

## Checkstyle
#echo "Writing coverage and unit testing report to tst/reports/${FLDR}/checkstyle.txt."
## shellcheck disable=SC2046
#echo $(header "Coverage and Unit") >> "tst/reports/${FLDR}/checkstyle.txt"
#pycodestyle --statistics ./src ./tst/api ./tst/util tst/models >> "tst/reports/${FLDR}/checkstyle.txt"
#echo "done."
#
## Bug Checking
#echo "Writing coverage and unit testing report to tst/reports/${FLDR}/bugreport.txt."
## shellcheck disable=SC2046
#echo $(header "Coverage and Unit") >> "tst/reports/${FLDR}/bugreport.txt"
#pylint -v -E --ignore=[,models,tst] -j 0 --suggestion-mode=y -e --report=yes upmed-api >> "tst/reports/${FLDR}/bugreport.txt"
#echo "done."

# Run unit tests
echo "Writing unit testing report to tst/reports/${FLDR}/unittests.txt."
# shellcheck disable=SC2046
echo $(header "Unit Tests") >> "tst/reports/${FLDR}/unittest.txt"
python ./src/app.py
#python -m unittest discover ./tst >> "tst/reports/${FLDR}/unittests.txt"
read
echo "done."
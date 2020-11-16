TS=$(date +%s)
FLDR="report-${TS}"
function header() {
    echo "============ upmed-web $1 Report Generated on ${TS} ============"
    echo '\n\n'
}
# Create output folder
mkdir "tst/Reports/${FLDR}"

# Linting
echo "Writing coverage and unit testing report to tst/reports/${FLDR}/coverage.txt."
# shellcheck disable=SC2046
echo $(header "Coverage and Unit") >> "tst/reports/${FLDR}/coverage.txt"
pylint pylint -v --ignore=[,models,tst] -j 0 --suggestion-mode=y -e -r y upmed-api >> "tst/reports/${FLDR}/linting.txt"
echo "done."

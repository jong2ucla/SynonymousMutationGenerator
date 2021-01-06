from flask import Flask, request

from processing import AATranslate, AltCodon, SameChecker

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route("/", methods=["GET", "POST"])
def mainpage():
    if request.method == "POST":
        ErrorMessage = "Sorry, your input DNA sequence was not formatted correctly. Make sure you avoided all non-ATGC characters, had no line breaks/spaces, and your sequence was a multiple of 3 in codon reading frame 1. Please try again."
        InputDNA = None
        TransRNAiResSeq = None
        TranslatedProtein = None
        TransRNAiResSeq = None
        RNAiResSeq = "ERROR"
        ProtLength = "ERROR"
        NumberBasesSame = None
        NumberBasesDifferent = "ERROR"
        DifferencePercentage = "ERROR"
        InputDNALength = "ERROR"
        InputDNA = request.form['UserInputDNA']
        InputDNA = InputDNA.upper()
        allowedcharacters = set("ACTG")
        if len(InputDNA)%3 == 0 and allowedcharacters.issuperset(InputDNA) == True:
            TranslatedProtein = AATranslate(InputDNA)
            RNAiResSeq = AltCodon(InputDNA)
            TransRNAiResSeq = AATranslate(RNAiResSeq)
            ProtLength = len(TranslatedProtein)
            InputDNALength = len(InputDNA)
            NumberBasesSame = SameChecker(str(InputDNA), str(RNAiResSeq))
            NumberBasesDifferent = int(InputDNALength - NumberBasesSame)
            DifferencePercentage = round((int(NumberBasesDifferent))/(int(InputDNALength))*100,2)
            ErrorMessage = ""
        if TransRNAiResSeq == TranslatedProtein:
            return '''
                <html>
                    <body>
                        <p><h2>{errormessage1}</h2></p>
                        <p>Your input DNA is:</p>
                        <p>{result0}</p>
                        <p>This input DNA sequence is <b>{result4}</b> base pairs. </p>
                        <p>The amino acid translation of your input DNA is:</p>
                        <p>{result1}</p>
                        <p>This translation corresponds to <b>{result3}</b> amino acid residues. </p>
                        <p>Your synonymous, RNAi-resistant DNA is:</p>
                        <p>{result2}</p>
                        <p>This tool changed <b>{result5}</b> nucleotide bases, which means <b>{result6}</b>% of your input DNA bases have been changed.</p>
                        <p>Note that your original RNAi sequence may be longer than your input DNA sequence.</p>
                        <p>This tool already checked to make sure the amino acid translation of the output DNA matched the translation of your input DNA.</p>
                        <p><a href="/">Click here to run another sequence </a>
                    </body>
                </html>
            '''.format(result0=InputDNA, result1=TranslatedProtein, result2=RNAiResSeq, result3=ProtLength, result4=InputDNALength, result5=NumberBasesDifferent, result6=DifferencePercentage, errormessage1=ErrorMessage)
    return '''
        <html>
            <body>
                <p><h1>Synonymous Mutation Generator</h1></p>
                <p><h2>About</h2></p>
                <p><h3>This tool takes a protein coding DNA sequence and generates silent mutations (human codon optimized) to output a synonymous DNA sequence.</h3></p>
                <p>This tool uses the standard codon table and does not consider the mitochondrial codon system.</p>
                <p>If the input sequence is an RNAi target, this tool can be used to generate an RNAi-resistant sequence that preserves protein coding sequence.</p>
                <p><h2>Usage</h2></p>
                <p>Your input sequence should be in codon reading frame 1 and a multiple of 3.</p>
                <p>Your input sequence should not have line breaks/spaces and should not have characters other than ACTG. It should also not contain a stop codon. </p>
                <p><b>Example of good input: </b>GGCCGTGAAGAAACCATTAATGGCTCC</p>
                <p>Check out the manuscript (with lots of worked examples) <a href="https://www.biorxiv.org/content/10.1101/2021.01.02.425100v1">at bioRxiv</a>, and please cite if you found this useful.</p>
                <form method="post" action=".">
                <p><h3>Enter your input sequence below.</h3></p>
                    <p><input name="UserInputDNA" /></p>
                    <p><input type="submit" value="Get synonymous DNA sequence" /></p>
                </form>
                <p>Last updated: 4 Jan 2021 to try error page</p>
            </body>
        </html>
    '''




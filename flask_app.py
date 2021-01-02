from flask import Flask, request

from processing import AATranslate, AltCodon, SameChecker

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route("/", methods=["GET", "POST"])
def mainpage():
    if request.method == "POST":
        InputDNA = None
        InputDNA = request.form['UserInputDNA']
        if len(InputDNA)%3 == 0:
            InputDNA = InputDNA.upper()
            TranslatedProtein = AATranslate(InputDNA)
            RNAiResSeq = AltCodon(InputDNA)
            TransRNAiResSeq = AATranslate(RNAiResSeq)
            ProtLength = len(TranslatedProtein)
            InputDNALength = len(InputDNA)
            NumberBasesSame = SameChecker(str(InputDNA), str(RNAiResSeq)) #these are updated on 2 Jan 2021
            NumberBasesDifferent = int(InputDNALength - NumberBasesSame) #these are updated on 2 Jan 2021
            DifferencePercentage = round((int(NumberBasesDifferent))/(int(InputDNALength))*100,2) #these are updated on 2 Jan 2021
        if TransRNAiResSeq == TranslatedProtein:
            return '''
                <html>
                    <body>
                        <p>Your input DNA is:</p>
                        <p>{result0}</p>
                        <p>This input DNA sequence is <b>{result4}</b> base pairs. </p>
                        <p>The amino acid translation of your input DNA is:</p>
                        <p>{result1}</p>
                        <p>This translation corresponds to <b>{result3}</b> residues. </p>
                        <p>Your synonymous, RNAi-resistant DNA is:</p>
                        <p>{result2}</p>
                        <p>This tool changed <b>{result5}</b> nucleotide bases, which means <b>{result6}</b>% of your input DNA bases have been changed.</p>
                        <p>Note that your original RNAi sequence may be longer than your input DNA sequence.</p>
                        <p>This tool already checked to make sure the amino acid translation of the output DNA matched the translation of your input DNA.</p>
                        <p><a href="/">Click here to run another sequence </a>
                    </body>
                </html>
            '''.format(result0=InputDNA, result1=TranslatedProtein, result2=RNAiResSeq, result3=ProtLength, result4=InputDNALength, result5=NumberBasesDifferent, result6=DifferencePercentage)
    return '''
        <html>
            <body>
                <p><h1>Synonymous Mutation Generator</h1></p>
                <p><h2>About</h2></p>
                <p><h3>This tool takes a protein coding DNA sequence and generates silent mutations (human codon optimized) to output a synonymous DNA sequence.</h3></p>
                <p>This tool uses the standard codon table and does not consider the mitochondrial codon system.</p>
                <p>If the input sequence is an RNAi target, this tool can be used to generate an RNAi-resistant sequence that preserves protein coding sequence.</p>
                <p><h2>Usage</h2></p>
                <p><h3>Enter your input sequence below.</h3></p>
                <p>Your input sequence should be in all upper case, codon reading frame 1, and a multiple of 3.</p>
                <p>Your input sequence should not have line breaks/spaces and should not have characters other than ACTG. It should also not contain a stop codon. </p>
                <p><b>This form does not (yet) check for invalid inputs, so double-check to make sure everything is formatted correctly.</b></p>
                <p>If there is a formatting error, the web page will crash instead of displaying an error message. Just reload and try again :) </p>
                <form method="post" action=".">
                    <p><input name="UserInputDNA" /></p>
                    <p><input type="submit" value="Get RNAi-resistant sequence" /></p>
                </form>
                <p>Last updated: 2 Jan 2021 to include the difference counter</p>
            </body>
        </html>
    '''




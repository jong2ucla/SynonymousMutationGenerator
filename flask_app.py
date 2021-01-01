#OK. I don't really know what I'm doing here, but let's role with it.
#My goal is to use HTML to provide a framework to allow a user to input a given DNA sequence, feed that into the Python script, and then spit out the resulting RNAi-resistant DNA sequence.
#Most of the direction here I am taking from https://blog.pythonanywhere.com/169/, Turning a Python script into a website

from flask import Flask, request

from processing import AATranslate, AltCodon

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
                        <p>This tool already checked to make sure the amino acid translation of the output DNA matched the translation of your input DNA.</p>
                        <p><a href="/">Click here to run another sequence </a>
                    </body>
                </html>
            '''.format(result0=InputDNA, result1=TranslatedProtein, result2=RNAiResSeq, result3=ProtLength, result4=InputDNALength)
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
            </body>
        </html>
    '''




#OK. I don't really know what I'm doing here, but let's role with it.
#My goal is to use HTML to provide a framework to allow a user to input a given DNA sequence, feed that into the Python script, and then spit out the resulting RNAi-resistant DNA sequence.
#Most of the direction here I am taking from https://blog.pythonanywhere.com/169/, Turning a Python script into a website

from flask import Flask, request

from processing import AATranslate, AltCodon #these are the two functions I defined that will input a protein coding DNA sequence and output (1) amino acids or (2) a synonymous DNA sequence.  

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route("/", methods=["GET", "POST"])
def mainpage():
    if request.method == "POST":
        InputDNA = None
        InputDNA = request.form['UserInputDNA'] #"UserInputDNA' is what I called what the user will enter into the form.
        if len(InputDNA)%3 == 0: #This checks to make sure the user's input DNA was a multiple of three. If so, it will perform three functions: (1) translate the user's sequence, (2) generate the synonymous DNA sequence, (2.5) translate the synonymous DNA sequence, and (3) check that the translation of the input user sequence and output synonymous sequence are the same.
            TranslatedProtein = AATranslate(InputDNA) 
            RNAiResSeq = AltCodon(InputDNA)
            TransRNAiResSeq = AATranslate(RNAiResSeq)
        if TransRNAiResSeq == TranslatedProtein:
            return '''
                <html>
                    <body>
                        <p>Your input DNA is: {result0}</p>
                        <p>The amino acid translation of your input DNA is: {result1}</p>
                        <p>Your synonymous, RNAi-resistant DNA is: {result2}</p>
                        <p>This tool already checked to make sure the amino acid translation of the output DNA matched the translation of your input DNA.</p>
                        <p><a href="/">Click here to run another sequence </a>
                    </body>
                </html>
            '''.format(result0=InputDNA, result1=TranslatedProtein, result2=RNAiResSeq) #Here is where you tell the HTML what each thing in brackets should be
    return '''
        <html>
            <body>
                <p><h1>Silent Mutation Generator</h1></p>
                <p><h2>About</h2></p>
                <p><h3>This tool takes a protein coding DNA sequence and generates silent mutations (human codon optimized) to output a synonymous DNA sequence.</h3></p>
                <p>If the input sequence is an RNAi target, this tool can be used to generate an RNAi-resistant sequence that preserves protein coding sequence.</p>
                <p><h2>Usage</h2></p>
                <p><h3>Enter your input sequence below.</h3></p>
                <p>Your input sequence should be in all upper case, codon reading frame 1, and a multiple of 3.</p>
                <p>Your input sequence should not have line breaks/spaces and should not have characters other than ACTG. It should also not contain a stop codon. </p>
                <p><h3>This form does not (yet) check for invalid inputs, so double-check to make sure everything is formatted correctly.</h3></p>
                <p>If there is a formatting error, the web page will crash instead of displaying an error message. Just reload and try again :) </p>
                <form method="post" action=".">
                    <p><input name="UserInputDNA" /></p>
                    <p><input type="submit" value="Get RNAi-resistant sequence" /></p>
                </form>
            </body>
        </html>
    '''




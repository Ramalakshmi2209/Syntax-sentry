from flask import Flask, render_template, request
import language_tool_python
import spacy

app = Flask(__name__, template_folder='app/templates')
language_tool = language_tool_python.LanguageTool('en-US')
nlp = spacy.load('en_core_web_sm')

def custom_correction(text):
    return text.replace("ovr", "over")

def perform_nlp_analysis(text):
    doc = nlp(text)
    
    
    pos_tags = [(token.text, token.pos_) for token in doc]
    named_entities = [(ent.text, ent.label_) for ent in doc.ents]
    
    return pos_tags, named_entities

@app.route('/')
def index():
    return render_template('app/index.html')

@app.route('/check', methods=['POST'])
def check():
    input_text = request.form['input_text']
    
    
    language_tool_matches = language_tool.check(input_text)
    corrected_text = language_tool.correct(input_text)

    
    corrected_text = custom_correction(corrected_text)

   
    pos_tags, named_entities = perform_nlp_analysis(corrected_text)

    return render_template('app/result.html', 
                           original_text=input_text, 
                           corrected_text=corrected_text,
                           language_tool_matches=language_tool_matches,
                           pos_tags=pos_tags,
                           named_entities=named_entities)

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, request, render_template, flash, session
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import InputRequired
from werkzeug.utils import secure_filename
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.document_loaders import PyPDFLoader
from langchain.indexes.vectorstore import VectorstoreIndexCreator
from langchain.chains.question_answering import load_qa_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms import OpenAI
import os

tiktoken.encoding_for_model('gpt-3.5-turbo')
tokenizer = tiktoken.get_encoding('cl100k_base')

def tiktoken_len(text):
    tokens = tokenizer.encode(
        text,
        disallowed_special=()
    )
    return len(tokens)

from langchain.text_splitter import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=400,
    chunk_overlap=20,
    length_function=tiktoken_len,
    separators=["\n\n", "\n", " ", ""]
)
app = Flask(__name__)

app.secret_key = 'chatbot'
env_config = os.getenv("APP_SETTINGS", "config.DevelopmentConfig")
app.config.from_object(env_config)
os.environ["OPENAI_API_KEY"] = app.config.get("SECRET_KEY")
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')

class UploadForm(FlaskForm):
    file = FileField('PDF File', validators=[InputRequired()])
    submit = SubmitField('Submit')


@app.route('/',methods=["GET","POST"])
def home():
    form = UploadForm()
    if form.validate_on_submit():
        file = form.file.data
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash ('File upload successfully!')
        session["filename"]=filename
    return render_template('index.html', form=form, filename=session.get("filename", None))

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    filename = session.get("filename",None)
    loader = PyPDFLoader(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    index_creator = VectorstoreIndexCreator()
    docsearch = index_creator.from_loaders([loader])
    chunks = text_splitter.split(loader.load())
    answers = []
    for chunk in chunks:
        docs = docsearch.vectorstore.similarity_search(chunk)
        prompt = f"""
        Answer the question that is given under triple round brackets with maximum detail.
        Make the answer maximum detailed with respect to your capability.
        Follow the format of the answer that is given in the question, if no information is provided, you can use the format you think is best equipped according to question.
        ((({chunk})))
        """
        answer = chain.run(input_documents=docs, question=prompt)
        answers.append(answer)
        return str(answers)


if __name__ == "__main__":
    app.run()


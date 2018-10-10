from flask_wtf import Form
from codemirror import CodeMirrorTextarea
from wtforms.fields import SubmitField
from flask.ext.codemirror import CodeMirror
# mandatory
CODEMIRROR_LANGUAGES = ['python', 'html']
# optional
CODEMIRROR_THEME = '3024-day'
CODEMIRROR_ADDONS = (
			('ADDON_DIR','ADDON_NAME'),
)
app = Flask(__name__)
app.config.from_object(__name__)
codemirror = CodeMirror(app)


class MyForm(Form):
    source_code = CodeMirrorField(language='python', config={'lineNumbers' : 'true'})
    submit = SubmitField('Submit')
	
    @app.route('/', methods = ['GET', 'POST'])
    def index():
        form = MyForm()
        if form.validate_on_submit():
            text = form.source_code.data
        return render_template('index.html', form = form)

if __name__ == "__main__":
   app.run(host='0.0.0.0', threaded=True, port=8080, debug=True)
from flask import Flask, redirect, url_for
from config import DevelopmentConfig
from dotenv import load_dotenv
from blueprints.medicine_routes import medicine_bp
 
load_dotenv()
 
app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
 
# register blueprints
app.register_blueprint(medicine_bp)
 
 
@app.route('/')
def index():
    return redirect(url_for('medicine.search'))
 
 
if __name__ == '__main__':
    app.run(debug=True)
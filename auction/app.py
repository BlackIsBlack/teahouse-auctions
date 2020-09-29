from flask import Flask, render_template 

app = Flask(__name__) 

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return ('NOTFOUND')
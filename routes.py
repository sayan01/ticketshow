from flask import *
from flask_login import *
from models import *
from forms import *
from error import *
from datetime import timedelta
from werkzeug.utils import secure_filename
from datetime import datetime
import os
from app import app

#------------------------------------------------------------------------------------
# routes for admin
#------------------------------------------------------------------------------------

@app.route('/admin')
@login_required
def admin():
    if current_user.is_admin:
        return render_template("admin.html")
    else:
        return redirect(url_for('index'))


# Error pages ------------------------------------------------------------------------------------
# invalid url
@app.errorhandler(404)
def error404(e):
    return render_template("error/404.html", error=e), 404

# forbidden
@app.errorhandler(403)
def error403(e):
    return render_template("error/403.html", error=e), 403
    
# internal error
@app.errorhandler(500)
def error500(e):
    return render_template("error/500.html", error=e), 500
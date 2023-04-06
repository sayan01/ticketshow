from flask import render_template, url_for
from app import app

# Error pages ------------------------------------------------------------------------------------
# invalid url
@app.errorhandler(404)
def error404(e):
    return render_template('error.html', 
                           error_code=404, 
                           error_title='Page not found', 
                           error_message='The page you are looking for does not exist.<br><strong>'+e.description+'</strong>'
                        ), 404

# forbidden
@app.errorhandler(403)
def error403(e):
    return render_template('error.html',
                           error_code=403,
                           error_title='Access denied',
                           error_message='You do not have permission to access this page.<br><strong>'+e.description+'</strong><br><a href="'+url_for('login')+'">Login</a> with correct credentials to access this page.'
                        ), 403
    
# internal error
@app.errorhandler(500)
def error500(e):
    return render_template('error.html', 
                           error_code=500, 
                           error_title='Internal server error', 
                           error_message='An internal server error has occurred.<br><strong>'+e.description+'</strong><br>Try again later'
                        ), 500
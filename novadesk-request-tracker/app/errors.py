from flask import render_template


def register_error_handlers(app):
    @app.errorhandler(403)
    def forbidden(error):
        # Bewust algemene boodschap: gebruiker krijgt weinig context over rechten.
        return render_template("error.html", status_code=403, title="Action not allowed", message="This action could not be completed."), 403

    @app.errorhandler(404)
    def not_found(error):
        return render_template("error.html", status_code=404, title="Page not found", message="The requested page does not exist."), 404

    @app.errorhandler(500)
    def internal_error(error):
        return render_template("error.html", status_code=500, title="Something went wrong", message="A technical error occurred."), 500

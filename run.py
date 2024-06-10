from iswap import app 
from iswap.auth import auth_bp
from iswap.general import land_bp
from iswap.dashboard import dashboard_bp

# Register blueprints.
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(land_bp)
app.register_blueprint(dashboard_bp, url_prefix='/dashboard')

# Run application
if __name__ == '__main__':
  app.run(debug=True)
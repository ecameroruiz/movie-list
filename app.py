"""
Serve Flask App
"""

from waitress import serve
from init import create_app

# create app
app = create_app(config='production')

# serve app
if __name__ == "__main__":
    try:
        serve(app, host='0.0.0.0', port=app.config['PORT'])
    except Exception as e:
        app.logger.error(e)
        raise e

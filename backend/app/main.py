<<<<<<< HEAD
#!/usr/bin/env python3
"""
Emotional Support AI - Main Entry Point
This file can be used to run the application directly
"""

from app import create_app
import os

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
=======
#!/usr/bin/env python3
"""
Emotional Support AI - Main Entry Point
This file can be used to run the application directly
"""

from app import create_app
import os

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
>>>>>>> 6a97c5ff1caff98b22d3c35a1de0b0b2e5252662
    )
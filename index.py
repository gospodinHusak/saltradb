from app import app, display_page

import pages.charts.callbacks
import pages.table_constructor.callbacks
import filters.callbacks as callbacks

server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)
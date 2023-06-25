from app import app, display_page
import pages.sql_editor.callbacks 
import pages.table.callbacks
import pages.charts.callbacks

server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)
from app import app, display_page
import pages.sql_page.callbacks 
import pages.filtering_page.callbacks


server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)
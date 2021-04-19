import wikiflix

def main():
    app = app_aanmaken()
    app.run(debug=True, host="0.0.0.0")
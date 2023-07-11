from website import create_app

app = create_app()

if __name__ == "__main__":
    # rerun the server when we make any changes
    app.run(debug=False, host='0.0.0.0')
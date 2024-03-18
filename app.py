from routes import app, db, socketio
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True, host='192.168.1.241')
        socketio.run(app)

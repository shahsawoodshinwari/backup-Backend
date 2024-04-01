from Pulsse import pulsse_app


app = pulsse_app()


if __name__ == "__main__":
      app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
    #app.run(debug=False, port=5000, threaded=True)
    #app.run(debug=False, port=8000, threaded=True)

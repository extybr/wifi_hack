from app import app, free_port


def run(host: str, port: int) -> None:
    """
    Starts the flask-application on the given port.
    If the port is occupied by any process, terminates it.
    """
    free_port(port)
    app.config["WTF_CSRF_ENABLED"] = False
    # app.run(port=port)
    app.run(host=host, port=port)
    # app.run(host='127.0.0.1', port=port, debug=True)


if __name__ == '__main__':
    run('0.0.0.0', 3000)

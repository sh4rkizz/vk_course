import multiprocessing
def django_app(environ, start_response):
    print(multiprocessing.cpu_count())
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain')]
    start_response(status, response_headers)
    return [b"<ul><li></ul>"]
application = django_app

# -*- coding: utf-8 -*-
import falcon
import resources
from wsgiref import simple_server
import logging
import argparse
import models

logger = logging.getLogger('appserver')

models.initialize()

app = falcon.API()

app.add_route('/persons', resources.MultiplePersons())
app.add_route('/persons/{id}', resources.SinglePerson())

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=8000)
    parser.add_argument('--host', type=str, default='0.0.0.0')
    parser.add_argument('--debug', type=bool, default=True)
    parser.add_argument('--preloader', type=bool, default=True)
    args = parser.parse_args()

    logger.debug('Starting server on {}:{}'.format(args.host, args.port))
    httpd = simple_server.make_server(args.host, args.port, app)
    httpd.serve_forever()

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()
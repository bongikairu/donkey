#!/bin/bash
#gunicorn -w=1 --reload --access-logfile - --error-logfile - --log-level info test:app
gunicorn -w=4 -k eventlet -b 0.0.0.0:8080 -b unix:/tmp/gunicorn.sock --error-logfile - --log-level info test:app
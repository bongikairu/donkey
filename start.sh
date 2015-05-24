#!/bin/bash
#gunicorn -w=1 --reload --access-logfile - --error-logfile - --log-level info test:app
gunicorn -w=4 -k eventlet --error-logfile - --log-level info test:app
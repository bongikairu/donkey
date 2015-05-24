#!/bin/bash
#gunicorn -w=1 --reload --access-logfile - --error-logfile - --log-level info test:app
gunicorn -w=4 --reload --error-logfile - --log-level warning test:app
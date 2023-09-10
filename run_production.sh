#!/usr/bin/env bash

mkdir -p static/scss

node_modules/.bin/webpack build --mode production
node_modules/.bin/sass static/scss:static/css

gunicorn app:app

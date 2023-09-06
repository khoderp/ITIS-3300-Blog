#!/usr/bin/env bash

# Terminate webpack when sass exits
# https://stackoverflow.com/a/2173421
trap "trap - SIGTERM && kill -- -$$" SIGINT SIGTERM EXIT

mkdir -p static/scss

node_modules/.bin/webpack build --mode development --watch &
node_modules/.bin/sass --watch static/scss:static/css &

FLASK_DEBUG=true flask run

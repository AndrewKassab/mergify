#!/bin/bash

cd ./app
flask run &
cd ..
pytest ./tests/api
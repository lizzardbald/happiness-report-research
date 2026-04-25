#!/bin/bash

pwd

docker run -p 5555:8888 -v $(pwd):/research data-science
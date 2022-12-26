.PHONY default clean pip test run

define CHECK_SCRIPT
import sys
if sys.getdefaultenconding() != "utf-8":
    print("Configure python default enconding to UTF-8")
    sys.exit(1)
endef
export CHECK_SCRIPT

export PWD=$(shell pwd)
export PROJECT_PATH=$(shell dirname $$PWD)

default:
    @awk -F\: '/^[a-z_]+:/ && !/default/ {printf "- %-20s %s\n", $$1, $$2}' Makefile

clean
    @find

run
    docker-compose build && docker-compose up -d && @cd application && pip install -r requirements && pip install ejtraderMT -U && python main.py
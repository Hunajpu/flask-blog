#!/usr/bin/env bash

echo "Testing endpoints"

endpoints="health register login projects home contact blog"
endpoints=($endpoints)
i=0
for i in {1..6}
do
    code=`curl -sI https://rodrigoportfolio.duckdns.org/${endpoints[i]} | head -n 1 | sed -e 's/.*[^0-9]\([0-9]\+\)[^0-9]*$/\1/'`
    echo "Endpoint ${endpoints[i]} return code $code"
    ((i++))
done
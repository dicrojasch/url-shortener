#!/bin/bash

# sequential 50 requests
time cat urls.txt | xargs -I{} echo "time curl -X POST -d 'link={}' http://localhost:5000/api/v1/create ; echo \"______________________\""

# parallel 50 requests
time cat urls.txt | xargs -P32 -I{} echo "time curl -X POST -d 'link={}' http://localhost:5000/api/v1/create ; echo \"______________________\""

# sequential 100 requests
time cat urls.txt urls.txt | xargs -I{} echo "time curl -X POST -d 'link={}' http://localhost:5000/api/v1/create ; echo \"______________________\""

# parallel 100 requests
time cat urls.txt cat urls.txt | xargs -P32 -I{} echo "time curl -X POST -d 'link={}' http://localhost:5000/api/v1/create ; echo \"______________________\""

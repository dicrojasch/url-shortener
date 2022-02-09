#!/bin/bash

# sequential 50 requests
time cat urls.txt | xargs -I{} echo "time curl -X POST -d 'link={}' https://239m52oz3g.execute-api.us-east-1.amazonaws.com/api/v1/create ; echo \"______________________\""

# parallel 50 requests
time cat urls.txt | xargs -P32 -I{} echo "time curl -X POST -d 'link={}' https://239m52oz3g.execute-api.us-east-1.amazonaws.com/api/v1/create ; echo \"______________________\""

# sequential 100 requests
time cat urls.txt urls.txt | xargs -I{} echo "time curl -X POST -d 'link={}' https://239m52oz3g.execute-api.us-east-1.amazonaws.com/api/v1/create ; echo \"______________________\""

# parallel 100 requests
time cat urls.txt cat urls.txt | xargs -P32 -I{} echo "time curl -X POST -d 'link={}' https://239m52oz3g.execute-api.us-east-1.amazonaws.com/api/v1/create ; echo \"______________________\""

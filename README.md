# shellbin-server
A server used to manage shareable bins.

## Getting started
In order to use the server you can either build a Docker image on the code or run it directly by executing the preliminary operations in the Dockerfile and typing

    python app.py
    
Anyway, our advice is to build a Docker image.

## Endpoints
Here are the exposed endpoints:
- GET  /api/v1/bin/{string:slug} (given a string slug returns the corresponding bin. Slugs are generated by the server and returned whenever a new Bin is created)
- POST /api/v1/bin/new (for the bin creation)


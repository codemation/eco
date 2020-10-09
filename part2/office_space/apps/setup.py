
async def run(server):
    from fastapi import Request
    async def process_request(request: Request):
        json_body = None
        if 'content-length' in request.headers and request.headers['content-type'] == 'application/json':
            body = await request.body()
            json_body = json.loads(body) if len(body) > 0 else None
        return RequestStorage(
            request.url, 
            request.headers, 
            request.method, 
            json_body
            )
    server.process_request = process_request
    
    from apps.office import office
    await office.run(server)

    from apps.person import person
    await person.run(server)   
            
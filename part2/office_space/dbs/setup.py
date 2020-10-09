
async def run(server):
    server.data = dict()
    from dbs.office import office_db
    await office_db.run(server)
            

async def db_attach(server):
    db = server.data['office']
    if not 'offices' in db.tables:
        await db.create_table(
            'offices', [
                ('name', str, 'UNIQUE NOT NULL')
            ],
            'name',
            cache_enabled=True
        )
        pass # Enter db.create_table statement here


    server.offices = db.tables['offices']
async def db_attach(server):
    db = server.data['office']
    if not 'persons' in db.tables:
        await db.create_table(
            'persons', [
                ('name', str, 'UNIQUE NOT NULL'), 
                ('age', int),
                ('office', str, )
            ],
            'name',
            foreign_keys={
                    'office': {
                        'table': 'offices', 
                        'ref': 'name',
                        'mods': 'ON UPDATE CASCADE ON DELETE CASCADE'
                    }
            },
            cache_enabled=True
        )
    server.persons = db.tables['persons']
async def attach_tables(server):
    from dbs.office.tables import offices
    await offices.db_attach(server)
            
    from dbs.office.tables import persons
    await persons.db_attach(server)
            
async def run(server):
    import sys, os

    async def office_attach():
        config=dict()
            
        with open('.cmddir', 'r') as projDir:
            for projectPath in projDir:
                config['database'] = f'{projectPath}dbs/office/office'
                config['loop'] = server.event_loop
        #USE ENV PATH for PYQL library or /pyql/
        sys.path.append('/pyql/' if os.getenv('PYQL_PATH') == None else os.getenv('PYQL_PATH'))
        from aiopyql import data
        from . import setup
        server.data['office'] = await data.Database.create(**config)
        server.data['office'].enable_cache()
        await setup.attach_tables(server)
        return {"status": 200, "message": "office attached successfully"}, 200
    await office_attach()
            
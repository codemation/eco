def run(server):
    import os, uuid
    from fastapi.testclient import TestClient
    from fastapi.websockets import WebSocket
    import uvloop, asyncio, random
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    event_loop = asyncio.get_event_loop()
    server.event_loop = event_loop

    try:
        import os
        cmddirPath = None
        realPath = None
        with open('./.cmddir', 'r') as cmddir:
            for line in cmddir:
                cmddirPath = line
            realPath = str(os.path.realpath(cmddir.name)).split('.cmddir')[0]
        if not realPath == cmddirPath:
            print(f"NOTE: Project directory may have moved, updating project cmddir files from {cmddirPath} -> {realPath}")
            import os
            os.system("find . -name .cmddir > .proj_cmddirs")
            with open('.proj_cmddirs', 'r') as projCmdDirs:
                for f in projCmdDirs:
                    with open(f.rstrip(), 'w') as projCmd:
                        projCmd.write(realPath)
    except Exception as e:
        print("encountered exception when checking projPath")
        print(repr(e))
    async def setup():

        from dbs import setup as dbsetup # TOO DOO -Change func name later
        await dbsetup.run(server) # TOO DOO - Change func name later

        from apps import setup
        await setup.run(server)

    event_loop.create_task(
        setup()
    )
                
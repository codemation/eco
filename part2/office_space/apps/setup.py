
async def run(server):

    from apps.office import office
    await office.run(server)

    from apps.person import person
    await person.run(server)   
            
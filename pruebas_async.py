import asyncio
async def F(i):
    print("Procesando: {:}".format(i))
    await asyncio.sleep(i)
    print("Resultado: {:}".format(i+1))


async def main():
    await asyncio.gather(F(1),F(2),F(3))

asyncio.run(main())
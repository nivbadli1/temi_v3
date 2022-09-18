import asyncio

from temi import Temi

temi_ip_address = "172.20.10.7"
# t = Temi('ws://172.20.10.7:8175')
# await t.connect()

async def connect_temi():
    temi = Temi('ws://172.20.10.7:8175')
    await temi.connect()
    message = await temi.interface(url="https://meet.google.com/dsf-ciew-iyo").speak(sentence="Going to do a call").run()
    print(message)
if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(connect_temi())




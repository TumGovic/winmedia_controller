import asyncio
from winmedia_controller.media_controller import MediaController

async def print_media_info():
    controller = MediaController()
    while True:
        info = await controller.get_media_info()
        if info:
            print(f"Media Info: {info}")
        await asyncio.sleep(1)  # Check every second

async def main():
    controller = MediaController()
    await print_media_info()

if __name__ == "__main__":
    asyncio.run(main())
import asyncio
from xbox.sg.console import Console
import os
import dotenv

dotenv.load_dotenv()
XBOX_IP = os.getenv("XBOX_IP")
LIVE_ID = os.getenv("LIVE_ID").encode()

async def wake():
    try:
        consoles = await Console.discover(timeout=1)
        if consoles:
            console = consoles[0]
            print(f"Found console: {console}")
        else:
            console = Console(XBOX_IP, LIVE_ID)
            print("Console not found via discovery, sending direct wake...")
        
        await console.power_on()
        print("Power on sent successfully")

    except Exception as e:
        print(f"Failed to wake Xbox: {e}")

asyncio.run(wake())
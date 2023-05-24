import ssl
import asyncio
import platform
from controller.controller import Controller

if __name__ == "__main__":
    ssl._create_default_https_context = ssl._create_unverified_context
    # context = ssl.SSLContext()
    # context.verify_mode = ssl.CERT_NONE
    if "Windows" == platform.system():
        policy = asyncio.WindowsSelectorEventLoopPolicy()
        asyncio.set_event_loop_policy(policy)
    asyncio.run(Controller().main())

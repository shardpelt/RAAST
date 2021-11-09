import sys
sys.path.append("..")
import asyncio
from Boat.boat import Boat

if __name__ == '__main__':
    transat = Boat()
    transat.start()
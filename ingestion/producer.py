import asyncio
from pathlib import Path

FEED_PATH = Path(__file__).parent.parent / "data" / "sample_feed.txt"

async def produce_comments(queue: asyncio.Queue, delay: float = 2.0) -> None:
    with open(FEED_PATH, "r", encoding="utf-8") as file:
        for line in file:
            comment = line.strip()

            if not comment:
                continue

            await queue.put(comment)

            print(f'[PRODUCER] → "{comment}"')

            await asyncio.sleep(delay)
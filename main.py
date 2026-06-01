from dotenv import load_dotenv
load_dotenv()
import asyncio
from ingestion.producer import produce_comments
from agent.graph import app


async def consume(queue: asyncio.Queue) -> None:
    sequence = 0

    while True:
        comment = await queue.get()

        if comment is None:
            break

        result = await app.ainvoke({
            "comment": comment,
            "sequence": sequence
        })

        print("[CONSUMER] →", result)

        sequence += 1


async def main():
    queue = asyncio.Queue()

    producer_task = asyncio.create_task(produce_comments(queue))
    consumer_task = asyncio.create_task(consume(queue))

    # attendre que le producer finisse
    await producer_task

    # signal de fin du stream
    await queue.put(None)

    # attendre arrêt propre du consumer
    await consumer_task


if __name__ == "__main__":
    asyncio.run(main())
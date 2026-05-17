from dotenv import load_dotenv
load_dotenv()
import asyncio
from ingestion.producer import produce_comments
from extraction.ner import extract_event


async def consume(queue: asyncio.Queue) -> None:
    sequence = 0

    while True:
        comment = await queue.get()

        if comment is None:
            break

        event = await extract_event(comment, sequence)

        if event:
            print("[CONSUMER] →", event.model_dump())
        else:
            print("[CONSUMER] → event ignoré")

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
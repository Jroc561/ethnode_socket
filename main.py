import pprint
from datetime import datetime
from config import client
import asyncio

w3 = client()

# asynchronous defined function to loop
# this loop runs on a poll interval
async def log_loop(event_filter, poll_interval):
    while True:
        for slot in event_filter.get_new_entries():
            handle_event(w3.eth.get_block(slot, full_transactions=True)) #set full_transactions to True to get detailed transaction data, else it will only return the transaction hash
        await asyncio.sleep(poll_interval)


# define function to handle events and print to the console
def handle_event(block):
    timestamp = datetime.utcfromtimestamp(block['timestamp'])
    print(f"block number: {block['number']}, posted at {str(timestamp)}")
    pprint.pprint(w3.toJSON(block), width=250)
    print(f"block number: {block['number']}, had {str(len(block['transactions']))} transactions")
    print('\n')


def main():
    block_filter = w3.eth.filter('latest')
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(
            asyncio.gather(
                log_loop(block_filter, 2)))
    finally:
        # close loop to free up system resources
        loop.close()



if __name__ == '__main__':
    main()


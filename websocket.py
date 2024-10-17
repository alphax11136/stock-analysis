import asyncio
import websockets
import json
from fetch_data import fetch_all_stocks_data
from datetime import datetime
from dateutil.relativedelta import relativedelta
import tables
from config import get_server_url  # Import the function that fetches server details

today, near_expiry, mid_expiry, far_expiry = tables.expiries()

# Global variables to store the current expiry, expiry date, days left, and open factor
current_expiry = None
current_exp_date = None
no_of_days_left = None
open_factor = None  # Store the open factor

# List to keep track of connected clients
connected_clients = set()


async def handler(websocket):
    global current_expiry, current_exp_date, no_of_days_left, open_factor
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            parts = message.split(":")
            
            if len(parts) == 3:  # Ensure the message has the expected format
                expiry_option = parts[1]
                open_factor_str = parts[2]
                
                try:
                    open_factor = float(open_factor_str)  # Convert open factor to float
                except ValueError:
                    print(f"Invalid open factor received: {open_factor_str}")
                    continue  # Skip this message if the open factor is invalid
                
                # Determine expiry date based on the received expiry option
                if expiry_option == 'near':
                    current_expiry = datetime.now().strftime('%y%b').upper()
                    current_exp_date = near_expiry
                elif expiry_option == 'mid':
                    current_expiry = (datetime.now() + relativedelta(months=+1)).strftime('%y%b').upper()
                    current_exp_date = mid_expiry
                elif expiry_option == 'far':
                    current_expiry = (datetime.now() + relativedelta(months=+2)).strftime('%y%b').upper()
                    current_exp_date = far_expiry
                else:
                    print(f"Unknown expiry option received: {expiry_option}")
                    continue  # Skip this message if the expiry option is invalid

                # Calculate number of days left based on the expiry date
                exp_date_dt = datetime.strptime(current_exp_date, '%d-%m-%Y')
                today_date = datetime.today()
                no_of_days_left = (exp_date_dt - today_date).days
                print(f"Updated expiry: {current_expiry}, Expiry Date: {current_exp_date}, Days Left: {no_of_days_left}, Open Factor: {open_factor}")
            else:
                print(f"Received malformed message: {message}")
    finally:
        connected_clients.remove(websocket)


async def broadcast_data():
    global current_expiry, no_of_days_left, open_factor
    while True:
        if current_expiry and no_of_days_left is not None and open_factor is not None:  # Only fetch if all required values are set
            # Fetch stock data using the current expiry, number of days left, and open factor
            data = fetch_all_stocks_data(current_expiry, no_of_days_left, open_factor)
            message = json.dumps(data)

            tasks = [client.send(message) for client in connected_clients]
            if tasks:
                await asyncio.gather(*tasks)
        await asyncio.sleep(1)


async def main():
    # Start the WebSocket server
    # async with websockets.serve(handler, "localhost", 8765):
    async with websockets.serve(handler, "0.0.0.0", 8765):

        # Start broadcasting data
        await broadcast_data()

# Run the server
if __name__ == '__main__':
    asyncio.run(main())

from jinja2 import Environment, FileSystemLoader
from datetime import datetime, timedelta


def last_thursday_of_month(year, month):
    # Find the last day of the month
    next_month = month % 12 + 1
    year += (month // 12)
    first_day_of_next_month = datetime(year, next_month, 1)
    last_day_of_month = first_day_of_next_month - timedelta(days=1)

    # Find the last Thursday of the month
    offset = (last_day_of_month.weekday() - 3) % 7  # Thursday is weekday 3 (0=Monday)
    last_thursday = last_day_of_month - timedelta(days=offset)
    return last_thursday


def expiries():
    today = datetime.now()
    current_year = today.year
    current_month = today.month

    # Get the last Thursday of the current month
    near_expiry_month = last_thursday_of_month(current_year, current_month)

    # If today is after the last Thursday of the current month, skip to the next month
    if today > near_expiry_month:
        current_month += 1  # Shift to the next month

    # Get the last Thursday for the adjusted months
    near_expiry = last_thursday_of_month(current_year, current_month).strftime('%d-%m-%Y')
    mid_expiry = last_thursday_of_month(current_year, current_month + 1).strftime('%d-%m-%Y')
    far_expiry = last_thursday_of_month(current_year, current_month + 2).strftime('%d-%m-%Y')

    return today, near_expiry, mid_expiry, far_expiry


def update_index_html():
    # Define the values to pass to the template
    # today_date = datetime.now().date()
    today, near_expiry, mid_expiry, far_expiry = expiries()
    today_date = today.date()

    # Convert string dates to datetime objects
    near_expiry = datetime.strptime(near_expiry, '%d-%m-%Y').date()
    mid_expiry = datetime.strptime(mid_expiry, '%d-%m-%Y').date()
    far_expiry = datetime.strptime(far_expiry, '%d-%m-%Y').date()

    days_left_today = 0
    days_left_near = (near_expiry - today_date).days
    days_left_mid = (mid_expiry - today_date).days
    days_left_far = (far_expiry - today_date).days

    future_buy_exp = 550
    future_sell_exp = 2600
    cash_buy_exp = 800
    cash_sell_exp = 4000
    cash_dlv_buy_exp = 12000
    cash_dlv_sell_exp = 11500

    # Create a dictionary to hold the dynamic values
    context = {
        'today_date': today_date,
        'near_expiry': near_expiry,
        'mid_expiry': mid_expiry,
        'far_expiry': far_expiry,

        'days_left_today':days_left_today,
        'days_left_near':days_left_near,
        'days_left_mid':days_left_mid, 
        'days_left_far':days_left_far,

        'future_buy_exp': future_buy_exp,
        'future_sell_exp': future_sell_exp,
        'cash_buy_exp': cash_buy_exp,
        'cash_sell_exp': cash_sell_exp,
        'cash_dlv_buy_exp': cash_dlv_buy_exp,
        'cash_dlv_sell_exp': cash_dlv_sell_exp,
    }


    print(f'context : {context}')
    # Set up the Jinja2 environment to load the template
    env = Environment(loader=FileSystemLoader('.'))  # Look for templates in the current directory
    template = env.get_template('index.html')

    # Render the template with the context (dynamic values)
    rendered_html = template.render(context)

    # Write the rendered HTML back to the file or serve it
    with open('index.html', 'w') as f:
        f.write(rendered_html)

    print("index.html has been updated with dynamic content.")

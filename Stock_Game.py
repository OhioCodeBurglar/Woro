import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import random

# Define the stock symbols (tickers) of the companies you're interested in
stock_symbols = ["AAPL", "MSFT", "GOOGL"]  # Apple, Microsoft, Google

# Pick one stock randomly from the list
selected_stock_symbol = random.choice(stock_symbols)

# Fetch historical stock data for the selected stock for the past 6 months
data = yf.download(selected_stock_symbol, period="6mo")

# Create the figure and subplot for the chart
fig, ax = plt.subplots(figsize=(10, 6))

# Plot the closing prices
ax.plot(data.index, data['Close'], label='Closing Price', color='blue')
ax.set_xlabel('Date')
ax.set_ylabel('Price')
ax.set_title(f'Closing Prices of {selected_stock_symbol}')
ax.legend()
ax.grid(True)

# Remove the number in price by setting y-axis tick format to M for million
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x / 1e6)) + "M"))

# Define button callback functions
def check_company(event, company):
    if company == selected_stock_symbol:
        ax.set_title('YOU WIN')
    else:
        ax.set_title('YOU LOSE')
    plt.draw()

# Create buttons for each company
button_width = 0.2
button_height = 0.075
spacing = 0.1
button_x = 0.1
companies = ["Apple", "Microsoft", "Google"]
button_axes = []
for i, company in enumerate(stock_symbols):
    button_ax = plt.axes([button_x + i * (button_width + spacing), 0.05, button_width, button_height])
    button = Button(button_ax, companies[i], color='blue', hovercolor='lightblue')
    button.on_clicked(lambda event, comp=company: check_company(event, comp))
    button_axes.append(button_ax)

plt.tight_layout()  # Adjust layout to prevent overlapping
plt.show()


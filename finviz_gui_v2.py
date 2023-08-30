import tkinter as tk
from tkinter import ttk
from finvizfinance.screener.overview import Overview
import pandas as pd

# Load CSV data into a DataFrame
def load_csv_data(filename, encoding='utf-8'):
    data = pd.read_csv(filename, encoding=encoding)
    return data

# Apply Filters to Fetch Stock Data
def apply_filters():
    selected_options = {}
    for filter_name, filter_combobox in filter_comboboxes.items():
        selected_option = filter_combobox.get()
        if selected_option:  # Check if the option is not empty
            selected_options[filter_name] = selected_option

    if selected_options:
        foverview = Overview()  # Assuming you have an Overview class defined
        foverview.set_filter(filters_dict=selected_options)
        df = foverview.screener_view()

        result_text = "Selected Options:\n"
        for filter_name, selected_option in selected_options.items():
            result_text += f"{filter_name}: {selected_option}\n"

        result_label.config(text=result_text)

        # Save data to CSV
        df.to_csv('/home/yhs/Documents/Scripts/filtered_stock_data.csv', index=False)
    else:
        result_label.config(text="No valid filters selected.")
    loaded_data = load_csv_data('/home/yhs/Documents/Scripts/filtered_stock_data.csv')  # Use the correct filename
    update_treeview(loaded_data)

def update_treeview(stock_data):
    tree.delete(*tree.get_children())
    for _, row in stock_data.iterrows():
        row_dict = {col.strip(): val for col, val in row.items()}
        tree.insert("", "end", values=[
            row_dict['Ticker'], row_dict['Company'], row_dict['Sector'],
            row_dict['Industry'], row_dict['Country'], row_dict['Market Cap'],
            row_dict['P/E'], row_dict['Price'], row_dict['Change'], row_dict['Volume']
        ])

root = tk.Tk()
root.title("Stock Screener")
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.geometry("%dx%d" % (width, height))

canvas = tk.Canvas(root)
canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

scrollbar = ttk.Scrollbar(root, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=frame, anchor="nw")

# Your filters dictionary
filters = {
    'Exchange': ['Any', 'AMEX', 'NASDAQ', 'NYSE'],
    'Index': ['Any', 'S&P 500', 'DJIA'],
    'Sector': ['Any', 'Basic Materials', 'Communication Services', 'Consumer Cyclical', 'Consumer Defensive', 'Energy', 'Financial', 'Healthcare', 'Industrials', 'Real Estate', 'Technology', 'Utilities'],
    'Industry': ['Any', 'Stocks only (ex-Funds)', 'Exchange Traded Fund', 'Advertising Agencies', 'Aerospace & Defense', 'Agricultural Inputs', 'Airlines', 'Airports & Air Services', 'Aluminum', 'Apparel Manufacturing', 'Apparel Retail', 'Asset Management', 'Auto Manufacturers', 'Auto Parts', 'Auto & Truck Dealerships', 'Banks - Diversified', 'Banks - Regional', 'Beverages - Brewers', 'Beverages - Non-Alcoholic', 'Beverages - Wineries & Distilleries', 'Biotechnology', 'Broadcasting', 'Building Materials', 'Building Products & Equipment', 'Business Equipment & Supplies', 'Capital Markets', 'Chemicals', 'Closed-End Fund - Debt', 'Closed-End Fund - Equity', 'Closed-End Fund - Foreign', 'Coking Coal', 'Communication Equipment', 'Computer Hardware', 'Confectioners', 'Conglomerates', 'Consulting Services', 'Consumer Electronics', 'Copper', 'Credit Services', 'Department Stores', 'Diagnostics & Research', 'Discount Stores', 'Drug Manufacturers - General', 'Drug Manufacturers - Specialty & Generic', 'Education & Training Services', 'Electrical Equipment & Parts', 'Electronic Components', 'Electronic Gaming & Multimedia', 'Electronics & Computer Distribution', 'Engineering & Construction', 'Entertainment', 'Farm & Heavy Construction Machinery', 'Farm Products', 'Financial Conglomerates', 'Financial Data & Stock Exchanges', 'Food Distribution', 'Footwear & Accessories', 'Furnishings, Fixtures & Appliances', 'Gambling', 'Gold', 'Grocery Stores', 'Healthcare Plans', 'Health Information Services', 'Home Improvement Retail', 'Household & Personal Products', 'Industrial Distribution', 'Information Technology Services', 'Infrastructure Operations', 'Insurance Brokers', 'Insurance - Diversified', 'Insurance - Life', 'Insurance - Property & Casualty', 'Insurance - Reinsurance', 'Insurance - Specialty', 'Integrated Freight & Logistics', 'Internet Content & Information', 'Internet Retail', 'Leisure', 'Lodging', 'Lumber & Wood Production', 'Luxury Goods', 'Marine Shipping', 'Medical Care Facilities', 'Medical Devices', 'Medical Distribution', 'Medical Instruments & Supplies', 'Metal Fabrication', 'Mortgage Finance', 'Oil & Gas Drilling', 'Oil & Gas E&P', 'Oil & Gas Equipment & Services', 'Oil & Gas Integrated', 'Oil & Gas Midstream', 'Oil & Gas Refining & Marketing', 'Other Industrial Metals & Mining', 'Other Precious Metals & Mining', 'Packaged Foods', 'Packaging & Containers', 'Paper & Paper Products', 'Personal Services', 'Pharmaceutical Retailers', 'Pollution & Treatment Controls', 'Publishing', 'Railroads', 'Real Estate - Development', 'Real Estate - Diversified', 'Real Estate Services', 'Recreational Vehicles', 'REIT - Diversified', 'REIT - Healthcare Facilities', 'REIT - Hotel & Motel', 'REIT - Industrial', 'REIT - Mortgage', 'REIT - Office', 'REIT - Residential', 'REIT - Retail', 'REIT - Specialty', 'Rental & Leasing Services', 'Residential Construction', 'Resorts & Casinos', 'Restaurants', 'Scientific & Technical Instruments', 'Security & Protection Services', 'Semiconductor Equipment & Materials', 'Semiconductors', 'Shell Companies', 'Silver', 'Software - Application', 'Software - Infrastructure', 'Solar', 'Specialty Business Services', 'Specialty Chemicals', 'Specialty Industrial Machinery', 'Specialty Retail', 'Staffing & Employment Services', 'Steel', 'Telecom Services', 'Textile Manufacturing', 'Thermal Coal', 'Tobacco', 'Tools & Accessories', 'Travel Services', 'Trucking', 'Uranium', 'Utilities - Diversified', 'Utilities - Independent Power Producers', 'Utilities - Regulated Electric', 'Utilities - Regulated Gas', 'Utilities - Regulated Water', 'Utilities - Renewable', 'Waste Management'],
    'Country': ['Any', 'USA', 'Foreign (ex-USA)', 'Asia', 'Europe', 'Latin America', 'BRIC', 'Argentina', 'Australia', 'Bahamas', 'Belgium', 'BeNeLux', 'Bermuda', 'Brazil', 'Canada', 'Cayman Islands', 'Chile', 'China', 'China & Hong Kong', 'Colombia', 'Cyprus', 'Denmark', 'Finland', 'France', 'Germany', 'Greece', 'Hong Kong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Ireland', 'Israel', 'Italy', 'Japan', 'Kazakhstan', 'Luxembourg', 'Malaysia', 'Malta', 'Mexico', 'Monaco', 'Netherlands', 'New Zealand', 'Norway', 'Panama', 'Peru', 'Philippines', 'Portugal', 'Russia', 'Singapore', 'South Africa', 'South Korea', 'Spain', 'Sweden', 'Switzerland', 'Taiwan', 'Turkey', 'United Arab Emirates', 'United Kingdom', 'Uruguay'],
    'Market Cap.': ['Any', 'Mega ($200bln and more)', 'Large ($10bln to $200bln)', 'Mid ($2bln to $10bln)', 'Small ($300mln to $2bln)', 'Micro ($50mln to $300mln)', 'Nano (under $50mln)', '+Large (over $10bln)', '+Mid (over $2bln)', '+Small (over $300mln)', '+Micro (over $50mln)', '-Large (under $200bln)', '-Mid (under $10bln)', '-Small (under $2bln)', '-Micro (under $300mln)'],
    'P/E': ['Any', 'Low (<15)', 'Profitable (>0)', 'High (>50)', 'Under 5', 'Under 10', 'Under 15', 'Under 20', 'Under 25', 'Under 30', 'Under 35', 'Under 40', 'Under 45', 'Under 50', 'Over 5', 'Over 10', 'Over 15', 'Over 20', 'Over 25', 'Over 30', 'Over 35', 'Over 40', 'Over 45', 'Over 50'],
    'Forward P/E': ['Any', 'Low (<15)', 'Profitable (>0)', 'High (>50)', 'Under 5', 'Under 10', 'Under 15', 'Under 20', 'Under 25', 'Under 30', 'Under 35', 'Under 40', 'Under 45', 'Under 50', 'Over 5', 'Over 10', 'Over 15', 'Over 20', 'Over 25', 'Over 30', 'Over 35', 'Over 40', 'Over 45', 'Over 50'],
    'PEG': ['Any', 'Low (<1)', 'High (>2)', 'Under 1', 'Under 2', 'Under 3', 'Over 1', 'Over 2', 'Over 3'],
    'P/S': ['Any', 'Low (<1)', 'High (>10)', 'Under 1', 'Under 2', 'Under 3', 'Under 4', 'Under 5', 'Under 6', 'Under 7', 'Under 8', 'Under 9', 'Under 10', 'Over 1', 'Over 2', 'Over 3', 'Over 4', 'Over 5', 'Over 6', 'Over 7', 'Over 8', 'Over 9', 'Over 10'],
    'P/B': ['Any', 'Low (<1)', 'High (>5)', 'Under 1', 'Under 2', 'Under 3', 'Under 4', 'Under 5', 'Under 6', 'Under 7', 'Under 8', 'Under 9', 'Under 10', 'Over 1', 'Over 2', 'Over 3', 'Over 4', 'Over 5', 'Over 6', 'Over 7', 'Over 8', 'Over 9', 'Over 10'],
    'Price/Cash': ['Any', 'Low (<3)', 'High (>50)', 'Under 1', 'Under 2', 'Under 3', 'Under 4', 'Under 5', 'Under 6', 'Under 7', 'Under 8', 'Under 9', 'Under 10', 'Over 1', 'Over 2', 'Over 3', 'Over 4', 'Over 5', 'Over 6', 'Over 7', 'Over 8', 'Over 9', 'Over 10', 'Over 20', 'Over 30', 'Over 40', 'Over 50'],
    'Price/Free Cash Flow': ['Any', 'Low (<15)', 'High (>50)', 'Under 5', 'Under 10', 'Under 15', 'Under 20', 'Under 25', 'Under 30', 'Under 35', 'Under 40', 'Under 45', 'Under 50', 'Under 60', 'Under 70', 'Under 80', 'Under 90', 'Under 100', 'Over 5', 'Over 10', 'Over 15', 'Over 20', 'Over 25', 'Over 30', 'Over 35', 'Over 40', 'Over 45', 'Over 50', 'Over 60', 'Over 70', 'Over 80', 'Over 90', 'Over 100'],
    'EPS growththis year': ['Any', 'Negative (<0%)', 'Positive (>0%)', 'Positive Low (0-10%)', 'High (>25%)', 'Under 5%', 'Under 10%', 'Under 15%', 'Under 20%', 'Under 25%', 'Under 30%', 'Over 5%', 'Over 10%', 'Over 15%', 'Over 20%', 'Over 25%', 'Over 30%'],
    'EPS growthnext year': ['Any', 'Negative (<0%)', 'Positive (>0%)', 'Positive Low (0-10%)', 'High (>25%)', 'Under 5%', 'Under 10%', 'Under 15%', 'Under 20%', 'Under 25%', 'Under 30%', 'Over 5%', 'Over 10%', 'Over 15%', 'Over 20%', 'Over 25%', 'Over 30%'],
    'EPS growthpast 5 years': ['Any', 'Negative (<0%)', 'Positive (>0%)', 'Positive Low (0-10%)', 'High (>25%)', 'Under 5%', 'Under 10%', 'Under 15%', 'Under 20%', 'Under 25%', 'Under 30%', 'Over 5%', 'Over 10%', 'Over 15%', 'Over 20%', 'Over 25%', 'Over 30%'],
    'EPS growthnext 5 years': ['Any', 'Negative (<0%)', 'Positive (>0%)', 'Positive Low (<10%)', 'High (>25%)', 'Under 5%', 'Under 10%', 'Under 15%', 'Under 20%', 'Under 25%', 'Under 30%', 'Over 5%', 'Over 10%', 'Over 15%', 'Over 20%', 'Over 25%', 'Over 30%'],
    'Sales growthpast 5 years': ['Any', 'Negative (<0%)', 'Positive (>0%)', 'Positive Low (0-10%)', 'High (>25%)', 'Under 5%', 'Under 10%', 'Under 15%', 'Under 20%', 'Under 25%', 'Under 30%', 'Over 5%', 'Over 10%', 'Over 15%', 'Over 20%', 'Over 25%', 'Over 30%'],
    'EPS growthqtr over qtr': ['Any', 'Negative (<0%)', 'Positive (>0%)', 'Positive Low (0-10%)', 'High (>25%)', 'Under 5%', 'Under 10%', 'Under 15%', 'Under 20%', 'Under 25%', 'Under 30%', 'Over 5%', 'Over 10%', 'Over 15%', 'Over 20%', 'Over 25%', 'Over 30%'],
    'Sales growthqtr over qtr': ['Any', 'Negative (<0%)', 'Positive (>0%)', 'Positive Low (0-10%)', 'High (>25%)', 'Under 5%', 'Under 10%', 'Under 15%', 'Under 20%', 'Under 25%', 'Under 30%', 'Over 5%', 'Over 10%', 'Over 15%', 'Over 20%', 'Over 25%', 'Over 30%'],
    'Dividend Yield': ['Any', 'None (0%)', 'Positive (>0%)', 'High (>5%)', 'Very High (>10%)', 'Over 1%', 'Over 2%', 'Over 3%', 'Over 4%', 'Over 5%', 'Over 6%', 'Over 7%', 'Over 8%', 'Over 9%', 'Over 10%'],
    'Return on Assets': ['Any', 'Positive (>0%)', 'Negative (<0%)', 'Very Positive (>15%)', 'Very Negative (', 'Under -50%', 'Under -45%', 'Under -40%', 'Under -35%', 'Under -30%', 'Under -25%', 'Under -20%', 'Under -15%', 'Under -10%', 'Under -5%', 'Over +5%', 'Over +10%', 'Over +15%', 'Over +20%', 'Over +25%', 'Over +30%', 'Over +35%', 'Over +40%', 'Over +45%', 'Over +50%'],
    'Return on Equity': ['Any', 'Positive (>0%)', 'Negative (<0%)', 'Very Positive (>30%)', 'Very Negative (', 'Under -50%', 'Under -45%', 'Under -40%', 'Under -35%', 'Under -30%', 'Under -25%', 'Under -20%', 'Under -15%', 'Under -10%', 'Under -5%', 'Over +5%', 'Over +10%', 'Over +15%', 'Over +20%', 'Over +25%', 'Over +30%', 'Over +35%', 'Over +40%', 'Over +45%', 'Over +50%'],
    'Return on Investment': ['Any', 'Positive (>0%)', 'Negative (<0%)', 'Very Positive (>25%)', 'Very Negative (', 'Under -50%', 'Under -45%', 'Under -40%', 'Under -35%', 'Under -30%', 'Under -25%', 'Under -20%', 'Under -15%', 'Under -10%', 'Under -5%', 'Over +5%', 'Over +10%', 'Over +15%', 'Over +20%', 'Over +25%', 'Over +30%', 'Over +35%', 'Over +40%', 'Over +45%', 'Over +50%'],
    'Current Ratio': ['Any', 'High (>3)', 'Low (<1)', 'Under 1', 'Under 0.5', 'Over 0.5', 'Over 1', 'Over 1.5', 'Over 2', 'Over 3', 'Over 4', 'Over 5', 'Over 10'],
    'Quick Ratio': ['Any', 'High (>3)', 'Low (<0.5)', 'Under 1', 'Under 0.5', 'Over 0.5', 'Over 1', 'Over 1.5', 'Over 2', 'Over 3', 'Over 4', 'Over 5', 'Over 10'],
    'LT Debt/Equity': ['Any', 'High (>0.5)', 'Low (<0.1)', 'Under 1', 'Under 0.9', 'Under 0.8', 'Under 0.7', 'Under 0.6', 'Under 0.5', 'Under 0.4', 'Under 0.3', 'Under 0.2', 'Under 0.1', 'Over 0.1', 'Over 0.2', 'Over 0.3', 'Over 0.4', 'Over 0.5', 'Over 0.6', 'Over 0.7', 'Over 0.8', 'Over 0.9', 'Over 1'],
    'Debt/Equity': ['Any', 'High (>0.5)', 'Low (<0.1)', 'Under 1', 'Under 0.9', 'Under 0.8', 'Under 0.7', 'Under 0.6', 'Under 0.5', 'Under 0.4', 'Under 0.3', 'Under 0.2', 'Under 0.1', 'Over 0.1', 'Over 0.2', 'Over 0.3', 'Over 0.4', 'Over 0.5', 'Over 0.6', 'Over 0.7', 'Over 0.8', 'Over 0.9', 'Over 1'],
    'Gross Margin': ['Any', 'Positive (>0%)', 'Negative (<0%)', 'High (>50%)', 'Under 90%', 'Under 80%', 'Under 70%', 'Under 60%', 'Under 50%', 'Under 45%', 'Under 40%', 'Under 35%', 'Under 30%', 'Under 25%', 'Under 20%', 'Under 15%', 'Under 10%', 'Under 5%', 'Under 0%', 'Under -10%', 'Under -20%', 'Under -30%', 'Under -50%', 'Under -70%', 'Under -100%', 'Over 0%', 'Over 5%', 'Over 10%', 'Over 15%', 'Over 20%', 'Over 25%', 'Over 30%', 'Over 35%', 'Over 40%', 'Over 45%', 'Over 50%', 'Over 60%', 'Over 70%', 'Over 80%', 'Over 90%'],
    'Operating Margin': ['Any', 'Positive (>0%)', 'Negative (<0%)', 'Very Negative (', 'High (>25%)', 'Under 90%', 'Under 80%', 'Under 70%', 'Under 60%', 'Under 50%', 'Under 45%', 'Under 40%', 'Under 35%', 'Under 30%', 'Under 25%', 'Under 20%', 'Under 15%', 'Under 10%', 'Under 5%', 'Under 0%', 'Under -10%', 'Under -20%', 'Under -30%', 'Under -50%', 'Under -70%', 'Under -100%', 'Over 0%', 'Over 5%', 'Over 10%', 'Over 15%', 'Over 20%', 'Over 25%', 'Over 30%', 'Over 35%', 'Over 40%', 'Over 45%', 'Over 50%', 'Over 60%', 'Over 70%', 'Over 80%', 'Over 90%'],
    'Net Profit Margin': ['Any', 'Positive (>0%)', 'Negative (<0%)', 'Very Negative (', 'High (>20%)', 'Under 90%', 'Under 80%', 'Under 70%', 'Under 60%', 'Under 50%', 'Under 45%', 'Under 40%', 'Under 35%', 'Under 30%', 'Under 25%', 'Under 20%', 'Under 15%', 'Under 10%', 'Under 5%', 'Under 0%', 'Under -10%', 'Under -20%', 'Under -30%', 'Under -50%', 'Under -70%', 'Under -100%', 'Over 0%', 'Over 5%', 'Over 10%', 'Over 15%', 'Over 20%', 'Over 25%', 'Over 30%', 'Over 35%', 'Over 40%', 'Over 45%', 'Over 50%', 'Over 60%', 'Over 70%', 'Over 80%', 'Over 90%'],
    'Payout Ratio': ['Any', 'None (0%)', 'Positive (>0%)', 'Low (<20%)', 'High (>50%)', 'Over 0%', 'Over 10%', 'Over 20%', 'Over 30%', 'Over 40%', 'Over 50%', 'Over 60%', 'Over 70%', 'Over 80%', 'Over 90%', 'Over 100%', 'Under 10%', 'Under 20%', 'Under 30%', 'Under 40%', 'Under 50%', 'Under 60%', 'Under 70%', 'Under 80%', 'Under 90%', 'Under 100%'],
    'Insider Ownership': ['Any', 'Low (<5%)', 'High (>30%)', 'Very High (>50%)', 'Over 10%', 'Over 20%', 'Over 30%', 'Over 40%', 'Over 50%', 'Over 60%', 'Over 70%', 'Over 80%', 'Over 90%'],
    'Insider Transactions': ['Any', 'Very Negative (<20%)', 'Negative (<0%)', 'Positive (>0%)', 'Very Positive (>20%)', 'Under -90%', 'Under -80%', 'Under -70%', 'Under -60%', 'Under -50%', 'Under -45%', 'Under -40%', 'Under -35%', 'Under -30%', 'Under -25%', 'Under -20%', 'Under -15%', 'Under -10%', 'Under -5%', 'Over +5%', 'Over +10%', 'Over +15%', 'Over +20%', 'Over +25%', 'Over +30%', 'Over +35%', 'Over +40%', 'Over +45%', 'Over +50%', 'Over +60%', 'Over +70%', 'Over +80%', 'Over +90%'],
    'Institutional Ownership': ['Any', 'Low (<5%)', 'High (>90%)', 'Under 90%', 'Under 80%', 'Under 70%', 'Under 60%', 'Under 50%', 'Under 40%', 'Under 30%', 'Under 20%', 'Under 10%', 'Over 10%', 'Over 20%', 'Over 30%', 'Over 40%', 'Over 50%', 'Over 60%', 'Over 70%', 'Over 80%', 'Over 90%'],
    'Institutional Transactions': ['Any', 'Very Negative (<20%)', 'Negative (<0%)', 'Positive (>0%)', 'Very Positive (>20%)', 'Under -50%', 'Under -45%', 'Under -40%', 'Under -35%', 'Under -30%', 'Under -25%', 'Under -20%', 'Under -15%', 'Under -10%', 'Under -5%', 'Over +5%', 'Over +10%', 'Over +15%', 'Over +20%', 'Over +25%', 'Over +30%', 'Over +35%', 'Over +40%', 'Over +45%', 'Over +50%'],
    'Float Short': ['Any', 'Low (<5%)', 'High (>20%)', 'Under 5%', 'Under 10%', 'Under 15%', 'Under 20%', 'Under 25%', 'Under 30%', 'Over 5%', 'Over 10%', 'Over 15%', 'Over 20%', 'Over 25%', 'Over 30%'],
    'Analyst Recom.': ['Any', 'Strong Buy (1)', 'Buy or better', 'Buy', 'Hold or better', 'Hold', 'Hold or worse', 'Sell', 'Sell or worse', 'Strong Sell (5)'],
    'Option/Short': ['Any', 'Optionable', 'Shortable', 'Optionable and shortable'],
    'Earnings Date': ['Any', 'Today', 'Today Before Market Open', 'Today After Market Close', 'Tomorrow', 'Tomorrow Before Market Open', 'Tomorrow After Market Close', 'Yesterday', 'Yesterday Before Market Open', 'Yesterday After Market Close', 'Next 5 Days', 'Previous 5 Days', 'This Week', 'Next Week', 'Previous Week', 'This Month'],
    'Performance': ['Any', 'Today Up', 'Today Down', 'Today -15%', 'Today -10%', 'Today -5%', 'Today +5%', 'Today +10%', 'Today +15%', 'Week -30%', 'Week -20%', 'Week -10%', 'Week Down', 'Week Up', 'Week +10%', 'Week +20%', 'Week +30%', 'Month -50%', 'Month -30%', 'Month -20%', 'Month -10%', 'Month Down', 'Month Up', 'Month +10%', 'Month +20%', 'Month +30%', 'Month +50%', 'Quarter -50%', 'Quarter -30%', 'Quarter -20%', 'Quarter -10%', 'Quarter Down', 'Quarter Up', 'Quarter +10%', 'Quarter +20%', 'Quarter +30%', 'Quarter +50%', 'Half -75%', 'Half -50%', 'Half -30%', 'Half -20%', 'Half -10%', 'Half Down', 'Half Up', 'Half +10%', 'Half +20%', 'Half +30%', 'Half +50%', 'Half +100%', 'Year -75%', 'Year -50%', 'Year -30%', 'Year -20%', 'Year -10%', 'Year Down', 'Year Up', 'Year +10%', 'Year +20%', 'Year +30%', 'Year +50%', 'Year +100%', 'Year +200%', 'Year +300%', 'Year +500%', 'YTD -75%', 'YTD -50%', 'YTD -30%', 'YTD -20%', 'YTD -10%', 'YTD -5%', 'YTD Down', 'YTD Up', 'YTD +5%', 'YTD +10%', 'YTD +20%', 'YTD +30%', 'YTD +50%', 'YTD +100%'],
    'Performance 2': ['Any', 'Today Up', 'Today Down', 'Today -15%', 'Today -10%', 'Today -5%', 'Today +5%', 'Today +10%', 'Today +15%', 'Week -30%', 'Week -20%', 'Week -10%', 'Week Down', 'Week Up', 'Week +10%', 'Week +20%', 'Week +30%', 'Month -50%', 'Month -30%', 'Month -20%', 'Month -10%', 'Month Down', 'Month Up', 'Month +10%', 'Month +20%', 'Month +30%', 'Month +50%', 'Quarter -50%', 'Quarter -30%', 'Quarter -20%', 'Quarter -10%', 'Quarter Down', 'Quarter Up', 'Quarter +10%', 'Quarter +20%', 'Quarter +30%', 'Quarter +50%', 'Half -75%', 'Half -50%', 'Half -30%', 'Half -20%', 'Half -10%', 'Half Down', 'Half Up', 'Half +10%', 'Half +20%', 'Half +30%', 'Half +50%', 'Half +100%', 'Year -75%', 'Year -50%', 'Year -30%', 'Year -20%', 'Year -10%', 'Year Down', 'Year Up', 'Year +10%', 'Year +20%', 'Year +30%', 'Year +50%', 'Year +100%', 'Year +200%', 'Year +300%', 'Year +500%', 'YTD -75%', 'YTD -50%', 'YTD -30%', 'YTD -20%', 'YTD -10%', 'YTD -5%', 'YTD Down', 'YTD Up', 'YTD +5%', 'YTD +10%', 'YTD +20%', 'YTD +30%', 'YTD +50%', 'YTD +100%'],
    'Volatility': ['Any', 'Week - Over 3%', 'Week - Over 4%', 'Week - Over 5%', 'Week - Over 6%', 'Week - Over 7%', 'Week - Over 8%', 'Week - Over 9%', 'Week - Over 10%', 'Week - Over 12%', 'Week - Over 15%', 'Month - Over 2%', 'Month - Over 3%', 'Month - Over 4%', 'Month - Over 5%', 'Month - Over 6%', 'Month - Over 7%', 'Month - Over 8%', 'Month - Over 9%', 'Month - Over 10%', 'Month - Over 12%', 'Month - Over 15%'],
    'RSI (14)': ['Any', 'Overbought (90)', 'Overbought (80)', 'Overbought (70)', 'Overbought (60)', 'Oversold (40)', 'Oversold (30)', 'Oversold (20)', 'Oversold (10)', 'Not Overbought (<60)', 'Not Overbought (<50)', 'Not Oversold (>50)', 'Not Oversold (>40)'],
    'Gap': ['Any', 'Up', 'Up 0%', 'Up 1%', 'Up 2%', 'Up 3%', 'Up 4%', 'Up 5%', 'Up 6%', 'Up 7%', 'Up 8%', 'Up 9%', 'Up 10%', 'Up 15%', 'Up 20%', 'Down', 'Down 0%', 'Down 1%', 'Down 2%', 'Down 3%', 'Down 4%', 'Down 5%', 'Down 6%', 'Down 7%', 'Down 8%', 'Down 9%', 'Down 10%', 'Down 15%', 'Down 20%'],
    '20-Day Simple Moving Average': ['Any', 'Price below SMA20', 'Price 10% below SMA20', 'Price 20% below SMA20', 'Price 30% below SMA20', 'Price 40% below SMA20', 'Price 50% below SMA20', 'Price above SMA20', 'Price 10% above SMA20', 'Price 20% above SMA20', 'Price 30% above SMA20', 'Price 40% above SMA20', 'Price 50% above SMA20', 'Price crossed SMA20', 'Price crossed SMA20 above', 'Price crossed SMA20 below', 'SMA20 crossed SMA50', 'SMA20 crossed SMA50 above', 'SMA20 crossed SMA50 below', 'SMA20 crossed SMA200', 'SMA20 crossed SMA200 above', 'SMA20 crossed SMA200 below', 'SMA20 above SMA50', 'SMA20 below SMA50', 'SMA20 above SMA200', 'SMA20 below SMA200'],
    '50-Day Simple Moving Average': ['Any', 'Price below SMA50', 'Price 10% below SMA50', 'Price 20% below SMA50', 'Price 30% below SMA50', 'Price 40% below SMA50', 'Price 50% below SMA50', 'Price above SMA50', 'Price 10% above SMA50', 'Price 20% above SMA50', 'Price 30% above SMA50', 'Price 40% above SMA50', 'Price 50% above SMA50', 'Price crossed SMA50', 'Price crossed SMA50 above', 'Price crossed SMA50 below', 'SMA50 crossed SMA20', 'SMA50 crossed SMA20 above', 'SMA50 crossed SMA20 below', 'SMA50 crossed SMA200', 'SMA50 crossed SMA200 above', 'SMA50 crossed SMA200 below', 'SMA50 above SMA20', 'SMA50 below SMA20', 'SMA50 above SMA200', 'SMA50 below SMA200'],
    '200-Day Simple Moving Average': ['Any', 'Price below SMA200', 'Price 10% below SMA200', 'Price 20% below SMA200', 'Price 30% below SMA200', 'Price 40% below SMA200', 'Price 50% below SMA200', 'Price 60% below SMA200', 'Price 70% below SMA200', 'Price 80% below SMA200', 'Price 90% below SMA200', 'Price above SMA200', 'Price 10% above SMA200', 'Price 20% above SMA200', 'Price 30% above SMA200', 'Price 40% above SMA200', 'Price 50% above SMA200', 'Price 60% above SMA200', 'Price 70% above SMA200', 'Price 80% above SMA200', 'Price 90% above SMA200', 'Price 100% above SMA200', 'Price crossed SMA200', 'Price crossed SMA200 above', 'Price crossed SMA200 below', 'SMA200 crossed SMA20', 'SMA200 crossed SMA20 above', 'SMA200 crossed SMA20 below', 'SMA200 crossed SMA50', 'SMA200 crossed SMA50 above', 'SMA200 crossed SMA50 below', 'SMA200 above SMA20', 'SMA200 below SMA20', 'SMA200 above SMA50', 'SMA200 below SMA50'],
    'Change': ['Any', 'Up', 'Up 1%', 'Up 2%', 'Up 3%', 'Up 4%', 'Up 5%', 'Up 6%', 'Up 7%', 'Up 8%', 'Up 9%', 'Up 10%', 'Up 15%', 'Up 20%', 'Down', 'Down 1%', 'Down 2%', 'Down 3%', 'Down 4%', 'Down 5%', 'Down 6%', 'Down 7%', 'Down 8%', 'Down 9%', 'Down 10%', 'Down 15%', 'Down 20%'],
    'Change from Open': ['Any', 'Up', 'Up 1%', 'Up 2%', 'Up 3%', 'Up 4%', 'Up 5%', 'Up 6%', 'Up 7%', 'Up 8%', 'Up 9%', 'Up 10%', 'Up 15%', 'Up 20%', 'Down', 'Down 1%', 'Down 2%', 'Down 3%', 'Down 4%', 'Down 5%', 'Down 6%', 'Down 7%', 'Down 8%', 'Down 9%', 'Down 10%', 'Down 15%', 'Down 20%'],
    '20-Day High/Low': ['Any', 'New High', 'New Low', '5% or more below High', '10% or more below High', '15% or more below High', '20% or more below High', '30% or more below High', '40% or more below High', '50% or more below High', '0-3% below High', '0-5% below High', '0-10% below High', '5% or more above Low', '10% or more above Low', '15% or more above Low', '20% or more above Low', '30% or more above Low', '40% or more above Low', '50% or more above Low', '0-3% above Low', '0-5% above Low', '0-10% above Low'],
    '50-Day High/Low': ['Any', 'New High', 'New Low', '5% or more below High', '10% or more below High', '15% or more below High', '20% or more below High', '30% or more below High', '40% or more below High', '50% or more below High', '0-3% below High', '0-5% below High', '0-10% below High', '5% or more above Low', '10% or more above Low', '15% or more above Low', '20% or more above Low', '30% or more above Low', '40% or more above Low', '50% or more above Low', '0-3% above Low', '0-5% above Low', '0-10% above Low'],
    '52-Week High/Low': ['Any', 'New High', 'New Low', '5% or more below High', '10% or more below High', '15% or more below High', '20% or more below High', '30% or more below High', '40% or more below High', '50% or more below High', '60% or more below High', '70% or more below High', '80% or more below High', '90% or more below High', '0-3% below High', '0-5% below High', '0-10% below High', '5% or more above Low', '10% or more above Low', '15% or more above Low', '20% or more above Low', '30% or more above Low', '40% or more above Low', '50% or more above Low', '60% or more above Low', '70% or more above Low', '80% or more above Low', '90% or more above Low', '100% or more above Low', '120% or more above Low', '150% or more above Low', '200% or more above Low', '300% or more above Low', '500% or more above Low', '0-3% above Low', '0-5% above Low', '0-10% above Low'],
    'Pattern': ['Any', 'Horizontal S/R', 'Horizontal S/R (Strong)', 'TL Resistance', 'TL Resistance (Strong)', 'TL Support', 'TL Support (Strong)', 'Wedge Up', 'Wedge Up (Strong)', 'Wedge Down', 'Wedge Down (Strong)', 'Triangle Ascending', 'Triangle Ascending (Strong)', 'Triangle Descending', 'Triangle Descending (Strong)', 'Wedge', 'Wedge (Strong)', 'Channel Up', 'Channel Up (Strong)', 'Channel Down', 'Channel Down (Strong)', 'Channel', 'Channel (Strong)', 'Double Top', 'Double Bottom', 'Multiple Top', 'Multiple Bottom', 'Head & Shoulders', 'Head & Shoulders Inverse'],
    'Candlestick': ['Any', 'Long Lower Shadow', 'Long Upper Shadow', 'Hammer', 'Inverted Hammer', 'Spinning Top White', 'Spinning Top Black', 'Doji', 'Dragonfly Doji', 'Gravestone Doji', 'Marubozu White', 'Marubozu Black'],
    'Beta': ['Any', 'Under 0', 'Under 0.5', 'Under 1', 'Under 1.5', 'Under 2', 'Over 0', 'Over 0.5', 'Over 1', 'Over 1.5', 'Over 2', 'Over 2.5', 'Over 3', 'Over 4', '0 to 0.5', '0 to 1', '0.5 to 1', '0.5 to 1.5', '1 to 1.5', '1 to 2'],
    'Average True Range': ['Any', 'Over 0.25', 'Over 0.5', 'Over 0.75', 'Over 1', 'Over 1.5', 'Over 2', 'Over 2.5', 'Over 3', 'Over 3.5', 'Over 4', 'Over 4.5', 'Over 5', 'Under 0.25', 'Under 0.5', 'Under 0.75', 'Under 1', 'Under 1.5', 'Under 2', 'Under 2.5', 'Under 3', 'Under 3.5', 'Under 4', 'Under 4.5', 'Under 5'],
    'Average Volume': ['Any', 'Under 50K', 'Under 100K', 'Under 500K', 'Under 750K', 'Under 1M', 'Over 50K', 'Over 100K', 'Over 200K', 'Over 300K', 'Over 400K', 'Over 500K', 'Over 750K', 'Over 1M', 'Over 2M', '100K to 500K', '100K to 1M', '500K to 1M', '500K to 10M'],
    'Relative Volume': ['Any', 'Over 10', 'Over 5', 'Over 3', 'Over 2', 'Over 1.5', 'Over 1', 'Over 0.75', 'Over 0.5', 'Over 0.25', 'Under 2', 'Under 1.5', 'Under 1', 'Under 0.75', 'Under 0.5', 'Under 0.25', 'Under 0.1'],
    'Current Volume': ['Any', 'Under 50K', 'Under 100K', 'Under 500K', 'Under 750K', 'Under 1M', 'Over 0', 'Over 50K', 'Over 100K', 'Over 200K', 'Over 300K', 'Over 400K', 'Over 500K', 'Over 750K', 'Over 1M', 'Over 2M', 'Over 5M', 'Over 10M', 'Over 20M'],
    'Price': ['Any', 'Under $1', 'Under $2', 'Under $3', 'Under $4', 'Under $5', 'Under $7', 'Under $10', 'Under $15', 'Under $20', 'Under $30', 'Under $40', 'Under $50', 'Over $1', 'Over $2', 'Over $3', 'Over $4', 'Over $5', 'Over $7', 'Over $10', 'Over $15', 'Over $20', 'Over $30', 'Over $40', 'Over $50', 'Over $60', 'Over $70', 'Over $80', 'Over $90', 'Over $100', '$1 to $5', '$1 to $10', '$1 to $20', '$5 to $10', '$5 to $20', '$5 to $50', '$10 to $20', '$10 to $50', '$20 to $50', '$50 to $100'],
    'Target Price': ['Any', '50% Above Price', '40% Above Price', '30% Above Price', '20% Above Price', '10% Above Price', '5% Above Price', 'Above Price', 'Below Price', '5% Below Price', '10% Below Price', '20% Below Price', '30% Below Price', '40% Below Price', '50% Below Price'],
    'IPO Date': ['Any', 'Today', 'Yesterday', 'In the last week', 'In the last month', 'In the last quarter', 'In the last year', 'In the last 2 years', 'In the last 3 years', 'In the last 5 years', 'More than a year ago', 'More than 5 years ago', 'More than 10 years ago', 'More than 15 years ago', 'More than 20 years ago', 'More than 25 years ago'],
    'Shares Outstanding': ['Any', 'Under 1M', 'Under 5M', 'Under 10M', 'Under 20M', 'Under 50M', 'Under 100M', 'Over 1M', 'Over 2M', 'Over 5M', 'Over 10M', 'Over 20M', 'Over 50M', 'Over 100M', 'Over 200M', 'Over 500M', 'Over 1000M'],
    'Float': ['Any', 'Under 1M', 'Under 5M', 'Under 10M', 'Under 20M', 'Under 50M', 'Under 100M', 'Over 1M', 'Over 2M', 'Over 5M', 'Over 10M', 'Over 20M', 'Over 50M', 'Over 100M', 'Over 200M', 'Over 500M', 'Over 1000M'],
}    

filter_comboboxes = {}
num_columns = 7  # 7 dropdowns per row
filters_per_row = len(filters) // num_columns
if len(filters) % num_columns != 0:
    filters_per_row += 1

row = 0
col = 0

for filter_name, options in filters.items():
    tk.Label(frame, text=filter_name).grid(row=row, column=col, sticky="w", padx=5, pady=5)
    
    combobox = ttk.Combobox(frame, values=options)
    combobox.grid(row=row, column=col + 1, padx=5, pady=5)
    filter_comboboxes[filter_name] = combobox

    row += 1
    if row >= filters_per_row:
        row = 0
        col += 2

apply_button = tk.Button(root, text="Apply Filters", command=apply_filters)
apply_button.pack(side=tk.BOTTOM, padx=10, pady=10)

result_label = tk.Label(root, text="Selected Options:")
result_label.pack(side=tk.BOTTOM, padx=10, pady=10)

tree = ttk.Treeview(root, columns=(
    "Ticker", "Company", "Sector", "Industry", 
    "Country", "Market Cap", "P/E", "Price", "Change", "Volume"
))
tree['show'] = 'headings'
tree.heading("#1", text="Ticker")
tree.heading("#2", text="Company")
tree.heading("#3", text="Sector")
tree.heading("#4", text="Industry")
tree.heading("#5", text="Country")
tree.heading("#6", text="Market Cap")
tree.heading("#7", text="P/E")
tree.heading("#8", text="Price")
tree.heading("#9", text="Change")
tree.heading("#10", text="Volume")
tree.pack(fill="both", expand=True, padx=20, pady=(0, 20))

root.mainloop()

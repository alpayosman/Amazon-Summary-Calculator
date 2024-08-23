import pandas as pd


def read_report(file_path):
    if file_path.endswith('.csv'):
        data = pd.read_csv(file_path)
    elif file_path.endswith('.xlsx'):
        data = pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file format")

    data['Date'] = pd.to_datetime(data['Date'], dayfirst=True, errors='coerce')

    data.dropna(subset=['Date'], inplace=True)

    if 'Order ID' in data.columns:
        data.drop(columns=['Order ID'], inplace=True)

    return data


def add_cost_production(data, begee_cost, buckhead_cost):
    data['Cost of Production'] = float(0)

    condition_begee = (data['Transaction type'] == 'Order Payment') & (
        data['Product Details'].str.contains('begee', case=False))
    condition_buckhead = (data['Transaction type'] == 'Order Payment') & (
        data['Product Details'].str.contains('buckhead', case=False))

    data.loc[condition_begee, 'Cost of Production'] = begee_cost
    data.loc[condition_buckhead, 'Cost of Production'] = buckhead_cost

    return data


def add_profit_column(data):
    data['Profit'] = data['Total (GBP)'] - data['Cost of Production']
    return data


def calculate_refund_sum(data):
    refund = data[(data['Transaction type'] == 'Refund')]
    total_refund_amount = refund['Total (GBP)'].sum()
    return total_refund_amount


def calculate_advertise_fees(data):
    adv = data[(data['Transaction type'] == 'Service Fees') & (data['Product Details'] == 'Cost of Advertising')]
    total_adv = adv['Total (GBP)'].sum()
    return total_adv


def calculate_storage_fees(data):
    storage = data[(data['Transaction type'] == 'Service Fees') & (data['Product Details'] == 'FBA storage fee')]
    long_storage = data[
        (data['Transaction type'] == 'Service Fees') & (data['Product Details'] == 'FBA Long-Term Storage Fee')]
    total = storage['Total (GBP)'].sum() + long_storage['Total (GBP)'].sum()
    return total


def calculate_other_fees(data):  # Sub, return and shipment
    fees = data[data['Transaction type'] == 'Service Fees']
    total_fees = fees['Total (GBP)'].sum() - (calculate_advertise_fees(data) + calculate_storage_fees(data))
    return total_fees


def calculate_total_fees(data):
    total = (calculate_advertise_fees(data) + calculate_storage_fees(data) + calculate_other_fees(data) +
             calculate_amz_sales_fees(data) + refund_fee(data) + calculate_other_sales_fees(data) +
             other_refund_fee(data))
    return total


def calculate_promotion_fee(data):
    promotion = data['Total promotional rebates'].sum()
    return promotion


def calculate_total_amount(data):
    order_sales = data[data['Transaction type'] == 'Order Payment']
    total = order_sales['Total product charges'].sum()
    return total


def calculate_net_total(data):
    total_net = data['Total (GBP)'].sum()
    return total_net


def calculate_amz_sales_fees(data):
    amz_fee = data[data['Transaction type'] == 'Order Payment']
    total = amz_fee['Amazon fees'].sum()
    return total


def calculate_other_sales_fees(data):
    amz_fee = data[data['Transaction type'] == 'Order Payment']
    total = amz_fee['Other'].sum()
    return total


def calculate_total_profit(data):
    total_profit = data['Profit'].sum()
    return total_profit


def calculate_total_cost_production(data):
    total_cost_of_production = data['Cost of Production'].sum()
    return -total_cost_of_production


def refund_fee(data):
    refund = data[data['Transaction type'] == 'Refund']
    refund_fees = refund['Amazon fees'].sum()
    return refund_fees


def other_refund_fee(data):
    refund = data[data['Transaction type'] == 'Refund']
    refund_fees = refund['Other'].sum()
    return refund_fees


def perform_calculations(data):
    calculations = {
        'Total Cost of Production': calculate_total_cost_production(data),
        'Other Fees': calculate_other_fees(data),
        'Storage Fees': calculate_storage_fees(data),
        'Advertising Fees': calculate_advertise_fees(data),
        'Amazon Sales Fees': calculate_amz_sales_fees(data),
        'Total Amazon Fees': calculate_total_fees(data),
        'Promotion Fees': calculate_promotion_fee(data),
        'Refund Amount': calculate_refund_sum(data),
        'Refund Fees': refund_fee(data),
        'Total Sales Amount': calculate_total_amount(data),
        'Net Total': calculate_net_total(data),
        'Total Profit': calculate_total_profit(data)
    }
    return calculations



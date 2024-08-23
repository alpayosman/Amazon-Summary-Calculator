import matplotlib.pyplot as plt
import io
import base64
import os
import numpy as np

from calculate import *

def graph(data, filename):
    transaction_types = [
        'Cost of Product',
        'Total Fee',
        'Promotion Fee',
        'Refund',
        'Sales',
        'After Purchased Fee',
        'Profit'
    ]

    totals = [
        calculate_total_cost_production(data),
        calculate_total_fees(data),
        calculate_promotion_fee(data),
        calculate_refund_sum(data),
        calculate_total_amount(data),
        calculate_net_total(data),
        calculate_total_profit(data)
    ]

    colors = [
        'red' if t in ['Cost of Product', 'Total Fee', 'Promotion Fee', 'Refund'] or (t == 'Profit' and totals[-1] < 0)
        else 'skyblue'
        for t in transaction_types
    ]

    fig, ax = plt.subplots(figsize=(20, 10), dpi=100)
    bars = ax.barh(transaction_types, totals, color=colors)
    ax.set_xlabel('Total Amount (GBP)')
    ax.set_title('Total Amount by Transaction Type')
    ax.invert_yaxis()

    for bar, total, transaction_type in zip(bars, totals, transaction_types):
        ax.text(total + 0.2 if total >= 0 else total - 0.2, bar.get_y() + bar.get_height()/2, f'{total:.2f}', va='center', ha='left' if total >= 0 else 'right')
        bar.set_gid(transaction_type)

    filepath = os.path.join('static', filename)
    plt.savefig(filepath)
    plt.close()
    return filepath

def percent_graph(data, filename):
    transaction_types = [
        'Refund',
        'Profit',
        'Amazon Sales Fee',
        'Advertising Cost'
    ]

    refund_percent = (calculate_refund_sum(data) / calculate_total_amount(data)) * 100
    profit_percent = (calculate_total_profit(data) / calculate_total_amount(data)) * 100
    amz_sales_fee_percent = ((calculate_amz_sales_fees(data) + calculate_other_sales_fees(data)) / calculate_total_amount(data)) * 100
    adv_percent = (calculate_advertise_fees(data) / calculate_total_amount(data)) * 100

    values = [
        refund_percent,
        profit_percent,
        amz_sales_fee_percent,
        adv_percent
    ]

    fig, ax = plt.subplots(figsize=(15, 6))
    bars = ax.bar(transaction_types, values, color=['red' if p < 0 else 'green' for p in values])
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2.0,
                 yval,
                 f'{yval:.2f}%',
                 va='bottom' if yval < 0 else 'top',
                 ha='center')

    ax.set_xlabel('Categories')
    ax.set_ylabel('Percentage')
    ax.set_title('Net Percentages by Category')

    ax.grid(False)
    ax.axhline(0, color='black', linewidth=0.8)

    filepath = os.path.join('static', filename)
    plt.savefig(filepath)
    plt.close()
    return filepath


def generate_individual_graph(data, column):
    if column == 'Amazon Fee':
        values = {
            'Advertising': calculate_advertise_fees(data),
            'AMZ Sales Fee': calculate_amz_sales_fees(data),
            'Other Sales Fee': calculate_other_sales_fees(data),
            'Other Fee': calculate_other_fees(data),
            'Storage Fee': calculate_storage_fees(data),
            'AMZ Refund Fee': refund_fee(data),
            'Other Refund Fee': other_refund_fee(data)
        }

        total_amazon_fee = sum(values.values())

        fig, ax = plt.subplots(figsize=(12, 6), dpi=100)

        labels = list(values.keys())
        amounts = list(values.values())

        running_total = np.cumsum([0] + amounts[:-1]).tolist()
        colors = ['green' if x > 0 else 'red' for x in amounts]

        bars = plt.bar(labels, amounts, color=colors, edgecolor='black')
        for bar, total in zip(bars, running_total):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'{bar.get_height():.2f}', ha='center', va='bottom')

        plt.xlabel('Categories')
        plt.ylabel('Amount (GBP)')
        plt.title('Waterfall Chart of Amazon Fees by Category')

        plt.text(0.95, 0.95, f'Total Amazon Fee: {total_amazon_fee:.2f} GBP', fontsize=12, ha='right', va='top', transform=ax.transAxes, bbox=dict(facecolor='white', alpha=0.5))

        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        graph_url = base64.b64encode(img.getvalue()).decode()
        plt.close()
        return 'data:image/png;base64,{}'.format(graph_url)

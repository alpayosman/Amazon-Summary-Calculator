import pandas as pd
from unittest.mock import patch
from calculate import *


def test_read_report():
    data = {
        'Date': ['01/01/2023', '02/01/2023', 'InvalidDate'],
        'Transaction type': ['Order Payment', 'Order Payment', 'Service Fees'],
        'Product Details': ['begee product', 'buckhead product', 'FBA storage fee'],
        'Order ID': [123, 124, 125],
        'Total (GBP)': [100, 150, 10]
    }
    df = pd.DataFrame(data)

    with patch('pandas.read_csv', return_value=df) as mock_read_csv, \
         patch('pandas.read_excel', return_value=df) as mock_read_excel:

        # Test CSV
        csv_data = read_report('test_report.csv')
        assert 'Order ID' not in csv_data.columns
        assert pd.to_datetime(csv_data['Date'], errors='coerce').notna().all()

        # Test Excel
        excel_data = read_report('test_report.xlsx')
        assert 'Order ID' not in excel_data.columns
        assert pd.to_datetime(excel_data['Date'], errors='coerce').notna().all()

    print("test_read_report passed")

def test_add_cost_production():
    data = pd.DataFrame({
        'Transaction type': ['Order Payment', 'Order Payment', 'Refund'],
        'Product Details': ['begee product', 'buckhead product', 'other product'],
        'Total (GBP)': [100, 150, -50]
    })
    begee_cost = 6
    buckhead_cost = 8
    data = add_cost_production(data, begee_cost, buckhead_cost)
    assert data['Cost of Production'].iloc[0] == begee_cost
    assert data['Cost of Production'].iloc[1] == buckhead_cost
    assert data['Cost of Production'].iloc[2] == 0

    print("test_add_cost_production passed")

def test_add_profit_column():
    data = pd.DataFrame({
        'Total (GBP)': [100, 150, -50],
        'Cost of Production': [6, 8, 0]
    })
    data = add_profit_column(data)
    assert data['Profit'].iloc[0] == 94
    assert data['Profit'].iloc[1] == 142
    assert data['Profit'].iloc[2] == -50

    print("test_add_profit_column passed")

def test_calculate_refund_sum():
    data = pd.DataFrame({
        'Transaction type': ['Order Payment', 'Refund', 'Refund'],
        'Total (GBP)': [100, -50, -20]
    })
    total_refund_amount = calculate_refund_sum(data)
    assert total_refund_amount == -70

    print("test_calculate_refund_sum passed")

def test_calculate_advertise_fees():
    data = pd.DataFrame({
        'Transaction type': ['Service Fees', 'Service Fees', 'Order Payment'],
        'Product Details': ['Cost of Advertising', 'Other Fee', 'Other Fee'],
        'Total (GBP)': [20, 30, 10]
    })
    total_adv = calculate_advertise_fees(data)
    assert total_adv == 20

    print("test_calculate_advertise_fees passed")

def test_calculate_storage_fees():
    data = pd.DataFrame({
        'Transaction type': ['Service Fees', 'Service Fees', 'Order Payment'],
        'Product Details': ['FBA storage fee', 'FBA Long-Term Storage Fee', 'Other Fee'],
        'Total (GBP)': [10, 20, 30]
    })
    total_storage_fees = calculate_storage_fees(data)
    assert total_storage_fees == 30

    print("test_calculate_storage_fees passed")

def test_calculate_other_fees():
    data = pd.DataFrame({
        'Transaction type': ['Service Fees', 'Service Fees', 'Order Payment'],
        'Product Details': ['Cost of Advertising', 'Other Fee', 'Other Fee'],
        'Total (GBP)': [20, 30, 10]
    })
    total_other_fees = calculate_other_fees(data)
    assert total_other_fees == 30

    print("test_calculate_other_fees passed")


def test_calculate_promotion_fee():
    data = pd.DataFrame({
        'Total promotional rebates': [10, 20, 30]
    })
    total_promotion_fee = calculate_promotion_fee(data)
    assert total_promotion_fee == 60

    print("test_calculate_promotion_fee passed")

def test_calculate_total_amount():
    data = pd.DataFrame({
        'Transaction type': ['Order Payment', 'Order Payment', 'Refund'],
        'Total product charges': [100, 150, 0]
    })
    total_amount = calculate_total_amount(data)
    assert total_amount == 250

    print("test_calculate_total_amount passed")

def test_calculate_net_total():
    data = pd.DataFrame({
        'Total (GBP)': [100, 150, -50]
    })
    total_net = calculate_net_total(data)
    assert total_net == 200

    print("test_calculate_net_total passed")

def test_calculate_amz_sales_fees():
    data = pd.DataFrame({
        'Transaction type': ['Order Payment', 'Order Payment', 'Refund'],
        'Amazon fees': [5, 10, 3]
    })
    amz_fees = calculate_amz_sales_fees(data)
    assert amz_fees == 15

    print("test_calculate_amz_sales_fees passed")

def test_calculate_other_sales_fees():
    data = pd.DataFrame({
        'Transaction type': ['Order Payment', 'Order Payment', 'Refund'],
        'Other': [1, 2, 1]
    })
    other_fees = calculate_other_sales_fees(data)
    assert other_fees == 3

    print("test_calculate_other_sales_fees passed")

def test_calculate_total_profit():
    data = pd.DataFrame({
        'Profit': [100, 150, -50]
    })
    total_profit = calculate_total_profit(data)
    assert total_profit == 200

    print("test_calculate_total_profit passed")

def test_calculate_total_cost_production():
    data = pd.DataFrame({
        'Cost of Production': [6, 8, 0]
    })
    total_cost_production = calculate_total_cost_production(data)
    assert total_cost_production == -14

    print("test_calculate_total_cost_production passed")

def test_refund_fee():
    data = pd.DataFrame({
        'Transaction type': ['Refund', 'Refund', 'Order Payment'],
        'Amazon fees': [5, 5, 10]
    })
    refund_fees = refund_fee(data)
    assert refund_fees == 10

    print("test_refund_fee passed")

def test_other_refund_fee():
    data = pd.DataFrame({
        'Transaction type': ['Refund', 'Refund', 'Order Payment'],
        'Other': [1, 1, 2]
    })
    other_refund_fees = other_refund_fee(data)
    assert other_refund_fees == 2

    print("test_other_refund_fee passed")

# Call the test functions
test_read_report()
test_add_cost_production()
test_add_profit_column()
test_calculate_refund_sum()
test_calculate_advertise_fees()
test_calculate_storage_fees()
test_calculate_other_fees()
test_calculate_promotion_fee()
test_calculate_total_amount()
test_calculate_net_total()
test_calculate_amz_sales_fees()
test_calculate_other_sales_fees()
test_calculate_total_profit()
test_calculate_total_cost_production()
test_refund_fee()
test_other_refund_fee()

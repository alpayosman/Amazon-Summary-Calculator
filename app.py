from flask import Flask, request, jsonify, render_template, send_file, url_for
from calculate import read_report, add_cost_production, add_profit_column, calculate_total_cost_production, calculate_total_amount, calculate_amz_sales_fees
from graph import graph, percent_graph, generate_individual_graph
from mongo import insert_metadata, get_all_metadata
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
STATIC_FOLDER = 'static'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if not os.path.exists(STATIC_FOLDER):
    os.makedirs(STATIC_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['STATIC_FOLDER'] = STATIC_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/graph', methods=['POST'])
def generate_graph():
    file = request.files['file']
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)  # Save the uploaded file to disk

    try:
        data = read_report(file_path)
    except ValueError as e:
        print(f"Error reading file: {e}")
        return render_template('index.html', error=str(e))

    begee_cost = float(request.form['begee_cost'])
    buckhead_cost = float(request.form['buckhead_cost'])

    data = add_cost_production(data, begee_cost, buckhead_cost)
    data = add_profit_column(data)

    # Calculate totals
    total_cost = calculate_total_cost_production(data)
    total_sales = calculate_total_amount(data)
    total_amazon_fees = calculate_amz_sales_fees(data)

    # Insert metadata into MongoDB
    insert_metadata(file.filename, total_cost, total_sales, total_amazon_fees)

    base_filename = os.path.splitext(file.filename)[0]
    main_graph_filename = f'{base_filename}_main_graph.png'
    percent_graph_filename = f'{base_filename}_percent_graph.png'
    individual_graph_filename = f'{base_filename}_amazon_fee_graph.png'

    main_graph_path = os.path.join(app.config['STATIC_FOLDER'], main_graph_filename)
    percent_graph_path = os.path.join(app.config['STATIC_FOLDER'], percent_graph_filename)
    individual_graph_path = os.path.join(app.config['STATIC_FOLDER'], individual_graph_filename)


    graph(data, main_graph_filename)
    percent_graph(data, percent_graph_filename)
    individual_graph_url = generate_individual_graph(data, 'Amazon Fee')

    main_graph_url = url_for('static', filename=main_graph_filename)
    percent_graph_url = url_for('static', filename=percent_graph_filename)

    return render_template('index.html',
                           main_graph_url=main_graph_url,
                           percent_graph_url=percent_graph_url,
                           individual_graph_url=individual_graph_url)

@app.route('/download/<filename>')
def download_file(filename):
    file_path = os.path.join(app.config['STATIC_FOLDER'], filename)
    return send_file(file_path, as_attachment=True)

@app.route('/metadata')
def list_metadata():
    metadata = get_all_metadata()
    return jsonify(metadata)

if __name__ == '__main__':
    app.run(debug=True)

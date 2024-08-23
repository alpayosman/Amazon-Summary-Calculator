from pymongo import MongoClient
from datetime import datetime

# Connect to MongoDB
client = MongoClient('localhost', 27017)
db = client['AMZ_Monthly_Summary']
metadata_collection = db['metadata']


def insert_metadata(file_name, total_cost, total_sales, total_amazon_fees):
    metadata = {
        'file_name': file_name,
        'total_cost': total_cost,
        'total_sales': total_sales,
        'total_amazon_fees': total_amazon_fees,
        'upload_date': datetime.now()
    }
    metadata_collection.insert_one(metadata)
    return metadata


def get_all_metadata():
    return list(metadata_collection.find())

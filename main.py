import logging
from datetime import date, datetime, timedelta
import json
from algoliasearch.search_client import SearchClient


TIMESTAMP = datetime.now().strftime('%Y%m%d_%H%M%S')

logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(process)d - %(levelname)s - %(message)s' , handlers=[
        logging.FileHandler(f"logs/debug_{TIMESTAMP}.log"),
        logging.StreamHandler()
            ] )


def load_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON in {file_path}: {e}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")


def upload_data_to_algolia(sampling:False):
    logging.info("Data Loader")

    # Define the algolia specific params
    algolia_user_id = "S4KTODFFQS"
    algolia_user_key = "335795b3c9211c913f13983449a33a0f"
    algolia_index_name = "ecom_index"
    query = "*"

    # Define the payload file and load the data as json object
    fileName = "data/payload.json"
    json_data = load_json_file(fileName)
    logging.info(f"Total length of records is : {len(json_data)}")

    # Extracting a sample for testing 
    if (sampling):
        upload_records = json_data[0:100]
        logging.info(f"Sample record count is : {len(upload_records)}")
    else:
        upload_records=json_data
        logging.info(f"Full load record count is : {len(upload_records)}")

    # Creating a client for interacting with Algolia
    try:
        client = SearchClient.create(algolia_user_id, algolia_user_key)
    except Exception as e:
        logging.error(f"An error occurred in getting Algolia client : {e}")       
        logging.error(f"Please check your internet connectivity and algolia credentials !!")       
        return

    # Create a new index and add a record
    index = client.init_index(algolia_index_name)
    index.save_objects(upload_records).wait()
    logging.info(f"Uploaded records: {len(upload_records)}")

    # Search the index and logging.info the results
    try:
        results = index.search(query)
    except Exception as e:
        logging.error(f"An error occurred in getting Algolia search response : {e}")       
        logging.error(f"Please check your internet connectivity and index name !!")       
        return

    # logging.info(results["hits"][0])
    logging.info("-"*100)
    logging.info(f"Search results hit count = {len(results['hits'])}")
    logging.info(f"Total number of results in index for query \"{query}\" is {results['nbHits']}")
    logging.info(f"Total number of pages for query \"{query}\" is {results['nbPages']}")

def main(args=None):
    logging.info("Main")

    # Pass true to load only first 100 records - default is False(full data load)
    upload_data_to_algolia(True)
    

if __name__ == "__main__":
    logging.info("="*100)
    main()
    logging.info("Exit")
    logging.info("="*100)
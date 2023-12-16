from flask import Flask, request, jsonify
from utils.data_handler import read_data, write_data

app = Flask(__name__)

# GET Endpoints

# Get all listings
@app.route('/listings', methods=['GET'])
def get_all_listings():
    data = read_data()
    if data is not None:
        return jsonify(data)  # Return the entire list of listings
    else:
        return jsonify({'error': 'Failed to fetch data'}), 500

# Get a listing by ID
@app.route('/listings/<int:listing_id>', methods=['GET'])
def get_listing_by_id(listing_id):
    data = read_data()
    if data is not None:
        for listing in data:
            if listing.get('id') == listing_id:
                return jsonify(listing)
        return jsonify({'error': 'Listing not found'}), 404
    else:
        return jsonify({'error': 'Failed to fetch data'}), 500

# Get listings filtered by query parameters
@app.route('/listings/filter', methods=['GET'])
def get_filtered_listings():
    data = read_data()
    listings = data['listings']

    # Example query parameters: price_gt, price_lt, neighborhood
    price_gt = request.args.get('price_gt')
    price_lt = request.args.get('price_lt')
    neighborhood = request.args.get('neighborhood')

    filtered_listings = []

    for listing in listings:
        if (price_gt is None or listing['price'] > int(price_gt)) and \
           (price_lt is None or listing['price'] < int(price_lt)) and \
           (neighborhood is None or listing['neighbourhood'] == int(neighborhood)):
            filtered_listings.append(listing)

    if not filtered_listings:
        # If no listings match the criteria, return a 400 response
        return jsonify({'error': 'No matching listings found'}), 400

    return jsonify(filtered_listings)

# POST Endpoint

# Create a new listing
@app.route('/listings', methods=['POST'])
def create_listing():
    data = read_data()
    if data is not None:
        try:
            new_listing = request.get_json()
            print("NEW Listing")
            print(new_listing)
            new_listing['id'] = len(data) + 1  # Use length of the list as the new ID
            data.append(new_listing)
            write_data(data)
            return jsonify(new_listing), 201  # 201 Created status code
        except Exception as e:
            return jsonify({'error': str(e)}), 400  # 400 Bad Request status code
    else:
        return jsonify({'error': 'Failed to fetch data'}), 500

# Create a new listing using /listing/search with search terms in JSON body
@app.route('/listing/search', methods=['POST'])
def search_listings():
    data = read_data()
    if data is not None:
        try:
            search_terms = request.get_json().get('search_terms', [])
            
            matching_listings = [
                listing for listing in data if any(
                    term.lower() in listing['name'].lower() for term in search_terms
                )
            ]

            return jsonify(matching_listings), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 400  # 400 Bad Request status code
    else:
        return jsonify({'error': 'Failed to fetch data'}), 500

# PATCH Endpoint

# Update an existing listing
@app.route('/listing/<int:listing_id>', methods=['PATCH'])
def update_listing(listing_id):
    data = read_data()
    if data is not None:
        try:
            updated_listing = request.get_json()

            # Find the index of the listing to update
            index_to_update = next((i for i, listing in enumerate(data) if listing['id'] == listing_id), None)

            if index_to_update is not None:
                # Update the listing
                data[index_to_update].update(updated_listing)

                # Save the updated data
                write_data(data)

                return jsonify(data[index_to_update]), 200
            else:
                return jsonify({'error': 'Listing not found'}), 404  # 404 Not Found status code
        except Exception as e:
            return jsonify({'error': str(e)}), 400  # 400 Bad Request status code
    else:
        return jsonify({'error': 'Failed to fetch data'}), 500

# DELETE Endpoint

# Delete an existing listing
@app.route('/listing/<int:listing_id>', methods=['DELETE'])
def delete_listing(listing_id):
    data = read_data()
    if data is not None:
        try:
            # Find the index of the listing to delete
            index_to_delete = next((i for i, listing in enumerate(data) if listing['id'] == listing_id), None)

            if index_to_delete is not None:
                # Delete the listing
                deleted_listing = data.pop(index_to_delete)

                # Save the updated data
                write_data(data)

                return jsonify(deleted_listing), 200
            else:
                return jsonify({'error': 'Listing not found'}), 404  # 404 Not Found status code
        except Exception as e:
            return jsonify({'error': str(e)}), 400  # 400 Bad Request status code
    else:
        return jsonify({'error': 'Failed to fetch data'}), 500

if __name__ == "__main__":
    app.run(debug=True)



#curl http://127.0.0.1:5000/listings
#curl http://127.0.0.1:5000/listings/2266768    
#curl 'http://127.0.0.1:5000/listings?price_gt=50&price_lt=150&neighborhood=78702'
#curl -X POST -H "Content-Type: application/json" -d '{"name": "New Listing", "price": 200}' http://127.0.0.1:5000/listings
#curl -X POST -H "Content-Type: application/json" -d '{"search_terms": ["2 bedroom", "1 bathroom"]}' http://127.0.0.1:5000/listing/search
#curl -X PATCH -H "Content-Type: application/json" -d '{"price": 250}' http://127.0.0.1:5000/listing/2266768
#curl -X DELETE http://127.0.0.1:5000/listing/2266768

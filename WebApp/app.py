from flask import Flask, render_template, request, redirect, url_for, session
import pg8000
import uuid
import logging

app = Flask(__name__, template_folder='src')

# Set up basic logging
logging.basicConfig(level=logging.DEBUG)

# Global variables
global db
global signedIn
global query_results
query_results = {}
signedIn = False  # Default


@app.route('/', methods=['GET', 'POST'])
def home():
    logging.debug("Home route hit!")
    
    if request.method == 'POST':
        global signedIn
        global db
        username = request.form.get('username')
        password = request.form.get('password')
        
        logging.debug(f"Received username: {username}, password: {'*' * len(password)}")
        
        try:
            db = pg8000.connect(user=username, password=password, host='codd.mines.edu', port=5433, database='csci403')
            signedIn = True
            logging.debug("Successfully signed in.")
            return redirect(url_for('form'))
        except Exception as e:
            signedIn = False
            logging.error(f"Error connecting to the database: {e}")
            return redirect(url_for('error'))
    
    return render_template('index.html')


@app.route('/form', methods=['GET', 'POST'])
def form():
    if not signedIn:
        logging.warning("User not signed in, redirecting to home.")
        return redirect(url_for('home'))

    if request.method == 'GET':
        logging.debug("Rendering form.")
        return render_template('form.html')

    # Process form on POST request
    logging.debug("Processing POST request from form.")
    
    global db
    cursor = db.cursor()

    # Collect form inputs
    incident_id = request.form.get('incident_id')
    reported_date = request.form.get('reported_date')
    incident_address = request.form.get('incident_address')
    victim_count = request.form.get('victim_count')
    is_traffic = request.form.get('is_traffic')
    offense_id = request.form.get('offense_id')
    offense_code = request.form.get('offense_code')
    precinct_id = request.form.get('precinct_id')
    district_id = request.form.get('district_id')
    neighborhood_id = request.form.get('neighborhood_id')
    group_by = request.form.getlist('group_by[]')

    # Construct the query
    query = """
        SELECT 
            *
        FROM 
            incident i
        LEFT JOIN offense o ON i.objectid = o.offense_id
        LEFT JOIN location l ON i.objectid = l.id
    """
    conditions = []

    # Add conditions based on user input
    if incident_id:
        conditions.append(f"i.objectid = {incident_id}")
    if reported_date:
        conditions.append(f"i.reported_date = '{reported_date}'")
    if incident_address:
        conditions.append(f"i.incident_address LIKE '%{incident_address}%'")
    if victim_count:
        conditions.append(f"i.victim_count = {victim_count}")
    if is_traffic:
        # Update to use BOOLEAN value TRUE or FALSE for 'is_traffic'
        conditions.append(f"i.is_traffic = {'TRUE' if is_traffic == '1' else 'FALSE'}")
    if offense_id:
        conditions.append(f"o.offense_id = {offense_id}")
    if offense_code:
        conditions.append(f"o.offense_code_extension LIKE '%{offense_code}%'")
    if precinct_id:
        conditions.append(f"l.precinct_id LIKE '%{precinct_id}%'")
    if district_id:
        conditions.append(f"l.district_id = '{district_id}'")
    if neighborhood_id:
        conditions.append(f"l.neighborhood_id LIKE '%{neighborhood_id}%'")

    # Append WHERE clause if there are conditions
    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    # Add GROUP BY clause if selected
    if group_by:
        query += " GROUP BY " + ", ".join(group_by)

    # Append WHERE clause if there are conditions
    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    # Add GROUP BY clause if selected
    if group_by:
        query += " GROUP BY " + ", ".join(group_by)

    logging.debug(f"Constructed Query: {query}")

    try:
        cursor.execute(query)
        results = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]

        # Store results with a unique key
        key = str(uuid.uuid4())
        query_results[key] = {'results': results, 'columns': column_names, 'query': query}

        logging.debug(f"Redirecting to results with key: {key}")
        return redirect(url_for('results', key=key))  
        # This sends a GET request to /results
    except Exception as e:
        logging.error(f"Error executing query: {e}")
        return f"An error occurred: {e}"


@app.route('/results', methods=['GET'])
def results():
    key = request.args.get('key')
    logging.debug(f"Received key in results route: {key}")
    
    global query_results

    if key in query_results:
        logging.debug(f"Found data for key: {key}")
        data = query_results.pop(key)  # Remove data after access

        if not data['results']:
            logging.debug("No results found for the query.")
            return render_template('results.html', message="No data found for your query.", query=data['query'])

        logging.debug(f"Displaying results for query: {data['query']}")
        return render_template('results.html', results=data['results'], columns=data['columns'], query=data['query'])
    
    logging.warning(f"No data found for the provided key: {key}")
    return "No results to display."


@app.route('/error')
def error():
    logging.error("An error occurred during database connection or query.")
    return render_template('error.html')


# Run the app
if __name__ == '__main__':
    app.run(debug=True)

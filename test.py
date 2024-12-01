from flask import Flask

# Create an instance of the Flask class for your web application
app = Flask(__name__)

# Define the route for the homepage
@app.route('/')
def home():
    return "Hello, World!"

# Run the app if this file is executed directly
if __name__ == '__main__':
    app.run(debug=True)

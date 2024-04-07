# Task Manager App 📋

Welcome to the Task Manager App! This Flask-based web application allows users to create, retrieve tasks,
create users, and generate tokens. The tasks are stored in a PostgreSQL database managed by ElephantSQL. The app is deployed on Render.com.

## Features

- Create tasks: Users can add tasks with relevant details.
- Retrieve tasks: Users can view their tasks and manage them accordingly.
- Create user: New users can register to access the app's features.
- Generate token: Users can obtain authentication tokens to access protected routes.

## Technologies Used

- Flask: Python-based web framework for building the backend.
- HTML: Markup language for structuring the frontend views.
- Bootstrap: Frontend framework for designing responsive and mobile-first websites.
- PostgreSQL: Relational database management system for storing tasks and user data.
- ElephantSQL: Hosted PostgreSQL service used for database management.
- Render.com: Cloud platform for hosting and deploying web applications.

## Deployment

The app is deployed on Render.com. You can access it [here](https://flask-tasks-apis.onrender.com/).

## Getting Started

To run the app locally, follow these steps:

1. Clone this repository to your local machine.
2. Install the necessary dependencies by running `pip install -r requirements.txt`.
3. Set up your PostgreSQL database either locally or using a service like ElephantSQL.
4. Update the database connection URL in the Flask app configuration.
5. Run the Flask application using `python app.py`.
6. Access the app in your web browser at `http://localhost:5000`.

## Usage

- Navigate to the respective routes for creating tasks, retrieving tasks, creating users, and generating tokens.
- Follow the on-screen instructions to interact with the app's features.

## Contributing

Contributions are welcome! Feel free to open a pull request with any improvements or features you'd like to add.


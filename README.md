# Banking Chatbot Application

This project is a simple banking chatbot web application built with Flask, AIML (Artificial Intelligence Markup Language), and SQLite. The application allows users to register, log in, access a personalized dashboard, and interact with a chatbot that responds to banking-related queries.

## Features

- **User Registration:** Users can create an account by providing personal details such as name, mobile number, national ID, gender, email, and account type.
  
- **User Login:** Users can log in using their national ID.
  
- **Dashboard:** Once logged in, users can view their profile details in a dashboard.
  
- **Chatbot Interaction:** Users can interact with a banking-focused chatbot that responds to queries. The chatbot has custom responses for login and registration queries and provides general assistance for banking questions.

## Technologies Used

- **Flask:** A lightweight web framework for Python used to build the web application.
  
- **AIML (Artificial Intelligence Markup Language):** Used for creating the chatbot logic.
  
- **SQLite:** A lightweight database used for storing user information.
  
- **HTML/CSS:** For creating the front-end pages.

## Project Structure

```plaintext
├── app.py               # Main Flask application file
├── schema.sql           # SQL schema file to initialize the database
├── templates/           # Directory containing HTML templates
│   ├── index.html       # Home page template
│   ├── register.html    # Registration page template
│   ├── login.html       # Login page template
│   ├── dashboard.html   # Dashboard page template
│   └── chat.html        # Chatbot page template
├── static/              # Directory containing static files (CSS, JavaScript)
│   └── style.css        # Stylesheet for the web pages
├── model/               # Directory containing AIML files and the brain dump
│   ├── std-startup.aiml # AIML file for chatbot startup logic
│   └── brain.dump       # AIML brain dump file
└── README.md            # Readme file for the project
```

## Setup and Installation

### Prerequisites

- Python 3.x
- Flask
- SQLite

### Installation Steps

1. **Clone the repository:**

   ```bash
   git clone https://github.com/parvvaresh/chat_bot.git
   cd chat_bot
   ```

2. **Install the required Python packages:**

   ```bash
   pip install flask aiml
   ```

3. **Initialize the database:**

   Ensure that the `schema.sql` file is in the root directory, then run:

   ```bash
   python -c 'from app import init_db; init_db()'
   ```

4. **Run the Flask application:**

   ```bash
   python app.py
   ```

   The application will be available at `http://127.0.0.1:5009/`.

### File Descriptions

- **`app.py`:** The main Python file containing all routes, functions, and logic for the web application.

- **`schema.sql`:** SQL script for creating the `users` table in the SQLite database.

- **`/templates`:** This directory contains all the HTML files for the application.

- **`/static`:** This directory is for static files like CSS and JavaScript.

- **`/model`:** This directory contains AIML files for the chatbot and the brain dump file.

### How the Application Works

1. **Registration:** Users register through the `/register` endpoint. The registration form collects basic user information, which is then stored in the SQLite database.

2. **Login:** Users log in through the `/login` endpoint using their national ID. If the national ID exists in the database, they are redirected to their dashboard.

3. **Dashboard:** The `/dashboard` endpoint shows user-specific information retrieved from the database.

4. **Chatbot Interaction:** Users can interact with the chatbot on the `/chat` page. The chatbot is powered by AIML and responds to banking-related queries. It also provides links to the login and registration pages when triggered by specific keywords.

### Customizing the Chatbot

- **AIML Files:** You can customize the chatbot's behavior by editing the AIML files in the `/model` directory.
  
- **Custom Responses:** The `get_chatbot_response` and `fix_respond` functions in `app.py` provide hooks for adding custom responses based on user input.

### Debugging and Development

- **Debug Mode:** The application runs in debug mode by default. To disable debug mode, set `debug=False` in the `app.run()` method in `app.py`.

- **Port Configuration:** The application is configured to run on port `5009`. You can change this by modifying the `port` variable.

### Security Notes

- **Secret Key:** Make sure to set a strong secret key for session management by replacing `'your_secret_key'` in `app.py` with a secure, random value.

### License

This project is open-source and available under the [MIT License](https://opensource.org/licenses/MIT).

---

Feel free to contribute by opening issues or submitting pull requests!
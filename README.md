# Mapping Project 2024

This is a webapp built in Django, designed to provide comprehensive information about various modules offered in different terms and years. The application allows users to filter modules based on the selected year and term, and view detailed information about each module.

## Features

- **Module Filtering**: Users can filter modules by year and term.
- **Detailed Module Information**: View detailed information about each module.
- **Graphical Representation**: Visualize module relationships and dependencies.

## Installation

### Prerequisites

- Python 3.x
- Django 5.x or higher
- Node.js and npm (for Tailwind CSS, only if you are going to alter HTML/CSS)
- Other dependencies listed in `requirements.txt`

### Steps

1. **Clone the repository**:

   ```sh
   git clone https://github.com/pz522-ic/mapping-project
   cd mapping-project
   ```

2. **Create a virtual environment**:

   ```sh
   python -m venv .venv
   ```

3. **Activate the virtual environment**:

   - On Windows:
     ```sh
     .venv/Scripts/activate
     ```
   - On macOS/Linux/bash:
     ```sh
     source .venv/bin/activate
     ```

4. **Install dependencies**:

   ```sh
   python -m pip install -r requirements.txt
   ```

5. **Apply migrations**:

   ```sh
   python manage.py migrate
   ```

6. **Install Node.js dependencies and Compile Tailwind CSS** (only if you are going to alter HTML/CSS):

   ```sh
   cd jstoolchain
   npm install
   npm run build:css
   cd ..
   ```

7. **Create a superuser**:

   ```sh
   python manage.py createsuperuser
   ```

8. **Run the development server**:

   ```sh
   python manage.py runserver
   ```

## Usage

1. Open your web browser and navigate to `http://127.0.0.1:8000/`.
2. Access the admin page at `http://127.0.0.1:8000/admin/` using the superuser credentials.

## Project Structure

- `modules/`: Contains the Django app for managing modules.
- `templates/`: Contains HTML templates for rendering the web pages.
- `static/`: Contains static files such as CSS, JavaScript, and images.
- `requirements.txt`: Lists the Python dependencies for the project.
- `tailwind.config.js`: Configuration file for Tailwind CSS.

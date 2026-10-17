# Simple Task Manager

A clean, beginner-friendly Task Manager web application built with Python (Flask) and SQLite. This project is structured specifically to help developers learn automated testing with **pytest** and prepare for building continuous integration (CI/CD) pipelines with **GitHub Actions**.

---

## Features

- **Task Overview**: View all tasks with real-time counters for Total, Pending, and Completed items.
- **Add Tasks**: Quick form to submit new tasks.
- **Validation**: Rejects empty submissions or whitespace-only inputs with helpful flash alerts.
- **Toggle Completion**: Mark tasks as completed (or switch back to pending) with a single click.
- **Delete Tasks**: Remove tasks with client-side confirmation.
- **Persistent Storage**: Lightweight SQLite database automatically initialized on startup.
- **Automated Tests**: Comprehensive test suite using pytest with clean test isolation.

---

## Tech Stack

- **Backend**: Python 3.8+, [Flask](https://flask.palletsprojects.com/)
- **Database**: SQLite3 (built into Python standard library)
- **Frontend**: HTML5, CSS3, minimal JavaScript
- **Testing**: [pytest](https://pytest.org/)

---

## Project Structure

```text
task-manager/
├── app.py              # Flask application, SQLite handling, and route definitions
├── requirements.txt    # Application and test dependencies
├── pytest.ini          # Pytest configuration (pythonpath, testpaths)
├── .gitignore          # Ignores venv, caches, and local .db files
├── README.md           # Setup, run, and CI/CD guide
├── templates/
│   ├── base.html       # Base HTML template with layout and flash notifications
│   └── index.html      # Main page: task list, form, and statistics
├── static/
│   ├── style.css       # Clean, responsive CSS styling
│   ├── app.js          # Minimal JavaScript for UX enhancements
│   └── script.js       # Forwarding script
└── tests/
    ├── conftest.py     # Pytest fixtures (isolated temporary database)
    └── test_app.py     # Automated unit and integration tests
```

---

## Getting Started

### 1. Prerequisites
- Python 3.8 or newer installed on your machine.
- Verify your installation:
  ```bash
  python --version
  ```

### 2. Set Up a Virtual Environment (Recommended)

Create a virtual environment:
```bash
python -m venv venv
```

Activate the virtual environment:
- **Windows (PowerShell):**
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
- **Windows (Command Prompt):**
  ```cmd
  venv\Scripts\activate.bat
  ```
- **macOS / Linux:**
  ```bash
  source venv/bin/activate
  ```

### 3. Install Dependencies

Install the required packages using `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 4. Run the Application

Start the Flask development server:
```bash
python app.py
```

Open your browser and navigate to:
```
http://127.0.0.1:5000
```

The database (`tasks.db`) will be automatically created on first launch.

---

## Running Automated Tests

The application includes an automated test suite designed to run in clean, isolated environments.

Run all tests with:
```bash
pytest -v
```
or:
```bash
python -m pytest -v
```

### What the tests cover:
- `test_index_empty`: Verifies the homepage loads correctly when no tasks exist.
- `test_add_task_success`: Verifies valid task creation, database persistence, and redirect.
- `test_add_empty_task_validation`: Verifies empty or whitespace-only inputs trigger validation errors.
- `test_mark_task_completed`: Verifies completing a task updates counters and UI state.
- `test_toggle_task_back_to_pending`: Verifies tasks can be toggled back to pending.
- `test_delete_task`: Verifies task deletion and counter updates.
- `test_complete_nonexistent_task`: Verifies 404 response for invalid task IDs.
- `test_delete_nonexistent_task`: Verifies 404 response for deleting non-existent task IDs.
- `test_multiple_tasks_and_statistics`: Verifies counters and task ordering across multiple tasks.

Each test run uses a temporary database created by `pytest`'s `tmp_path` fixture in [`tests/conftest.py`](file:///c:/Users/admin/Downloads/task-manager/tests/conftest.py), ensuring tests never interfere with your local development database.

---

## Ready for CI/CD: Next Steps

When you are ready to set up your first **GitHub Actions** CI workflow:

1. **Initialize Git**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Task Manager application with tests"
   ```
2. **Push to GitHub**:
   - Create a new repository on GitHub.
   - Add your remote and push (`git remote add origin <repo-url>` and `git push -u origin main`).
3. **Create the CI Workflow**:
   - Create a directory `.github/workflows/`.
   - Add a YAML file (e.g., `ci.yml`) that:
     1. Checks out the code (`actions/checkout`).
     2. Sets up Python (`actions/setup-python`).
     3. Installs dependencies (`pip install -r requirements.txt`).
     4. Runs the test suite (`pytest`).

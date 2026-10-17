import os
import sqlite3
from flask import (
    Flask,
    abort,
    current_app,
    flash,
    g,
    redirect,
    render_template,
    request,
    url_for,
)


def get_db():
    """Connect to the configured SQLite database and return the connection."""
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    """Close the database connection if it was opened."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    """Create the database tables if they do not exist."""
    db = get_db()
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            completed INTEGER NOT NULL DEFAULT 0,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        """
    )
    db.commit()


def create_app(test_config=None):
    """Application factory for the Task Manager Flask app."""
    app = Flask(__name__)

    # Default configuration
    default_db = os.path.join(app.root_path, "tasks.db")
    app.config.from_mapping(
        SECRET_KEY="dev-secret-key-for-task-manager",
        DATABASE=default_db,
    )

    if test_config is not None:
        app.config.from_mapping(test_config)

    # Register teardown function to clean up database connections
    app.teardown_appcontext(close_db)

    # Ensure tables exist on startup
    with app.app_context():
        init_db()

    @app.route("/")
    def index():
        """Display all tasks with summary statistics."""
        db = get_db()
        tasks = db.execute(
            "SELECT id, title, completed, created_at FROM tasks ORDER BY completed ASC, id DESC"
        ).fetchall()

        total_tasks = len(tasks)
        completed_tasks = sum(1 for task in tasks if task["completed"] == 1)
        pending_tasks = total_tasks - completed_tasks

        return render_template(
            "index.html",
            tasks=tasks,
            total_tasks=total_tasks,
            completed_tasks=completed_tasks,
            pending_tasks=pending_tasks,
        )

    @app.route("/add", methods=["POST"])
    def add_task():
        """Add a new task with validation."""
        title = request.form.get("title", "").strip()

        # Validation: Check for empty task submission
        if not title:
            flash("Task title cannot be empty! Please enter a task name.", "error")
            return redirect(url_for("index"))

        db = get_db()
        db.execute("INSERT INTO tasks (title, completed) VALUES (?, 0)", (title,))
        db.commit()

        flash("Task added successfully!", "success")
        return redirect(url_for("index"))

    @app.route("/complete/<int:task_id>", methods=["POST"])
    def toggle_task(task_id):
        """Mark a task as completed or toggle back to pending."""
        db = get_db()
        task = db.execute(
            "SELECT id, completed FROM tasks WHERE id = ?", (task_id,)
        ).fetchone()

        if task is None:
            abort(404, description=f"Task with ID {task_id} not found.")

        new_status = 0 if task["completed"] == 1 else 1
        db.execute(
            "UPDATE tasks SET completed = ? WHERE id = ?",
            (new_status, task_id),
        )
        db.commit()

        if new_status == 1:
            flash("Task marked as completed!", "success")
        else:
            flash("Task marked as pending!", "info")

        return redirect(url_for("index"))

    @app.route("/delete/<int:task_id>", methods=["POST"])
    def delete_task(task_id):
        """Delete an existing task."""
        db = get_db()
        task = db.execute(
            "SELECT id FROM tasks WHERE id = ?", (task_id,)
        ).fetchone()

        if task is None:
            abort(404, description=f"Task with ID {task_id} not found.")

        db.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        db.commit()

        flash("Task deleted successfully!", "success")
        return redirect(url_for("index"))

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)

from app import get_db


def test_index_empty(client):
    """Test that the index page loads successfully and displays the empty state."""
    response = client.get("/")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Task Manager" in html
    assert "No tasks yet" in html
    assert '<span class="stat-value" id="stat-total">0</span>' in html


def test_add_task_success(client):
    """Test adding a new task successfully."""
    response = client.post(
        "/add",
        data={"title": "Learn GitHub Actions"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Learn GitHub Actions" in html
    assert "Task added successfully!" in html
    assert '<span class="stat-value" id="stat-total">1</span>' in html
    assert '<span class="stat-value stat-pending" id="stat-pending">1</span>' in html


def test_add_empty_task_validation(client):
    """Test that empty or whitespace-only tasks are rejected with a helpful message."""
    # Test completely empty string
    response = client.post(
        "/add",
        data={"title": ""},
        follow_redirects=True,
    )
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Task title cannot be empty!" in html
    assert "No tasks yet" in html

    # Test whitespace-only string
    response = client.post(
        "/add",
        data={"title": "   \t  \n  "},
        follow_redirects=True,
    )
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Task title cannot be empty!" in html
    assert "No tasks yet" in html


def test_mark_task_completed(client):
    """Test marking a task as completed."""
    # Add a task
    client.post("/add", data={"title": "Write unit tests"})

    # Complete the task (id 1)
    response = client.post("/complete/1", follow_redirects=True)
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Task marked as completed!" in html
    assert '<span class="stat-value stat-completed" id="stat-completed">1</span>' in html
    assert '<span class="stat-value stat-pending" id="stat-pending">0</span>' in html
    assert "is-completed" in html


def test_toggle_task_back_to_pending(client):
    """Test toggling a completed task back to pending."""
    client.post("/add", data={"title": "Refactor code"})

    # Complete it first
    client.post("/complete/1")

    # Toggle back to pending
    response = client.post("/complete/1", follow_redirects=True)
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Task marked as pending!" in html
    assert '<span class="stat-value stat-pending" id="stat-pending">1</span>' in html
    assert '<span class="stat-value stat-completed" id="stat-completed">0</span>' in html


def test_delete_task(client):
    """Test deleting an existing task."""
    client.post("/add", data={"title": "Clean temporary files"})

    response = client.post("/delete/1", follow_redirects=True)
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Task deleted successfully!" in html
    assert "Clean temporary files" not in html
    assert "No tasks yet" in html


def test_complete_nonexistent_task(client):
    """Test that attempting to complete a non-existent task returns 404."""
    response = client.post("/complete/999")
    assert response.status_code == 404


def test_delete_nonexistent_task(client):
    """Test that attempting to delete a non-existent task returns 404."""
    response = client.post("/delete/999")
    assert response.status_code == 404


def test_multiple_tasks_and_statistics(client):
    """Test multiple tasks with correct status calculations."""
    tasks = ["Task 1", "Task 2", "Task 3"]
    for t in tasks:
        client.post("/add", data={"title": t})

    # Mark Task 2 (id=2) as completed
    client.post("/complete/2")

    response = client.get("/")
    assert response.status_code == 200
    html = response.get_data(as_text=True)

    assert '<span class="stat-value" id="stat-total">3</span>' in html
    assert '<span class="stat-value stat-pending" id="stat-pending">2</span>' in html
    assert '<span class="stat-value stat-completed" id="stat-completed">1</span>' in html
    for t in tasks:
        assert t in html

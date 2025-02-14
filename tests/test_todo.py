# tests/test_todo.py


def test_create_todo(client):
    """
    Test membuat todo baru (POST /todos).
    """
    # Aksi: buat todo
    response = client.post("/todos", json={"title": "Belajar Testing"})
    assert response.status_code == 201

    data = response.get_json()
    assert data["message"] == "Todo created successfully"
    assert data["data"]["title"] == "Belajar Testing"
    assert data["data"]["completed"] is False


def test_create_todo_invalid(client):
    """
    Test membuat todo dengan title kosong -> 400
    """
    response = client.post("/todos", json={"title": ""})
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    # Pastikan pesan error nya sesuai
    # (ini tergantung implementasi Anda di service/controller)
    # Contoh:
    assert data["error"] == "Title is required"


def test_get_all_todos(client):
    """
    Test membaca semua todo (GET /todos).
    Kita buat dulu beberapa todo sebelum memanggil GET.
    """
    # Arrange: buat 2 data
    client.post("/todos", json={"title": "Todo 1"})
    client.post("/todos", json={"title": "Todo 2"})

    # Act
    response = client.get("/todos")
    assert response.status_code == 200

    data = response.get_json()
    assert "data" in data
    assert isinstance(data["data"], list)
    # Seharusnya ada 2
    assert len(data["data"]) == 2


def test_get_todo_by_id(client):
    """
    Test membaca todo (GET /todos/<id>)
    """
    # Arrange: buat data dulu
    create_resp = client.post("/todos", json={"title": "My Todo"})
    create_data = create_resp.get_json()
    created_id = create_data["data"]["id"]

    # Act
    response = client.get(f"/todos/{created_id}")
    assert response.status_code == 200

    todo_data = response.get_json()
    # Pastikan data sesuai
    assert todo_data["id"] == created_id
    assert todo_data["title"] == "My Todo"
    assert todo_data["completed"] is False


def test_update_todo(client):
    """
    Test mengupdate todo (PUT /todos/<id>)
    """
    # Arrange: buat data
    create_resp = client.post("/todos", json={"title": "Old Title"})
    created_id = create_resp.get_json()["data"]["id"]

    # Act: update
    update_resp = client.put(
        f"/todos/{created_id}", json={"title": "Updated Title", "completed": True}
    )
    assert update_resp.status_code == 200

    update_data = update_resp.get_json()
    assert update_data["message"] == "Todo updated successfully"
    assert update_data["data"]["title"] == "Updated Title"
    assert update_data["data"]["completed"] is True


def test_delete_todo(client):
    """
    Test menghapus todo (DELETE /todos/<id>).
    """
    # Arrange: buat data
    create_resp = client.post("/todos", json={"title": "Will Delete"})
    created_id = create_resp.get_json()["data"]["id"]

    # Act: delete
    del_resp = client.delete(f"/todos/{created_id}")
    assert del_resp.status_code == 200

    del_data = del_resp.get_json()
    assert del_data["message"] == "Todo deleted successfully"

    # Cek GET => 404
    check_resp = client.get(f"/todos/{created_id}")
    assert check_resp.status_code == 404

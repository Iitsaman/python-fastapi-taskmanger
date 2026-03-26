import { useState, useEffect } from "react";
import { api } from "../api";

export default function AdminTasks() {
  const [tasks, setTasks] = useState([]);
  const [editingTaskId, setEditingTaskId] = useState(null);
  const [editingTaskTitle, setEditingTaskTitle] = useState("");

  const loadAllTasks = async () => {
    try {
      const res = await api.get("/tasks/all"); // admin-only
      setTasks(res.data);
    } catch (err) {
      alert("Failed to load all tasks (admin only)");
    }
  };

  const startEdit = (task) => {
    setEditingTaskId(task.id);
    setEditingTaskTitle(task.title);
  };

  const updateTask = async () => {
    if (!editingTaskTitle.trim()) {
      alert("Task title cannot be empty");
      return;
    }

    try {
      await api.put(`/tasks/${editingTaskId}`, { title: editingTaskTitle });
      setEditingTaskId(null);
      setEditingTaskTitle("");
      loadAllTasks();
    } catch (err) {
      console.log("Update error:", err.response?.data);
      alert("Failed to update task");
    }
  };

  const deleteTask = async (id) => {
    try {
      await api.delete(`/tasks/${id}`);
      loadAllTasks();
    } catch (err) {
      alert("Failed to delete task");
    }
  };

  const toggleCompleted = async (task) => {
    try {
      await api.put(`/tasks/${task.id}`, { completed: !task.completed });
      loadAllTasks();
    } catch (err) {
      alert("Failed to toggle completed");
    }
  };

  useEffect(() => { loadAllTasks(); }, []);

  return (
    <div>
      <h2>All Tasks (Admin)</h2>
      <ul>
        {tasks.map((task) => (
          <li key={task.id}>
            {editingTaskId === task.id ? (
              <>
                <input
                  value={editingTaskTitle}
                  onChange={(e) => setEditingTaskTitle(e.target.value)}
                />
                <button onClick={updateTask}>Save</button>
                <button onClick={() => setEditingTaskId(null)}>Cancel</button>
              </>
            ) : (
              <>
                <span
                  style={{ textDecoration: task.completed ? "line-through" : "none", cursor: "pointer" }}
                  onClick={() => toggleCompleted(task)}
                >
                  {task.title} (Owner: {task.owner})
                </span>
                <button onClick={() => startEdit(task)}>Edit</button>
                <button onClick={() => deleteTask(task.id)}>Delete</button>
              </>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}
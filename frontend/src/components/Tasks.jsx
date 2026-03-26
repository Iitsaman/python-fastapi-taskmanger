import { useState, useEffect } from "react";
import { api } from "../api";

export default function Tasks({ onLogout, isAdmin }) {
  const [tasks, setTasks] = useState([]);
  const [newTask, setNewTask] = useState("");

  // Edit states 
  const [editingTaskId, setEditingTaskId] = useState(null);
  const [editingTaskTitle, setEditingTaskTitle] = useState("");
  const [editingTaskDescription, setEditingTaskDescription] = useState("");
  const [editingTaskCompleted, setEditingTaskCompleted] = useState(false);

  // Load Tasks 
  const loadTasks = async () => {
    try {
      const url = isAdmin ? "/tasks/all" : "/tasks/";
      const res = await api.get(url);
      setTasks(res.data);
    } catch (err) {
      console.log("Load error:", err.response?.data);
      alert("Failed to load tasks");
    }
  };

  useEffect(() => {
    loadTasks();
  }, [isAdmin]);

  // Create
  const createTask = async () => {
    if (!newTask.trim()) return;

    try {
      await api.post("/tasks/", {
        title: newTask,
        description: "",
      });

      setNewTask("");
      loadTasks();
    } catch (err) {
      console.log("Create error:", err.response?.data);
      alert("Failed to create task");
    }
  };

  // Start Edit 
  const startEdit = (task) => {
    setEditingTaskId(task.id);
    setEditingTaskTitle(task.title);
    setEditingTaskDescription(task.description || "");
    setEditingTaskCompleted(task.completed || false);
  };

  //  Update 
  const updateTask = async () => {
    if (!editingTaskId) return;

    try {
      await api.put(`/tasks/${editingTaskId}`, {
        title: editingTaskTitle,
        description: editingTaskDescription,
        completed: editingTaskCompleted,
      });

      // Reset edit state
      setEditingTaskId(null);
      setEditingTaskTitle("");
      setEditingTaskDescription("");
      setEditingTaskCompleted(false);

      loadTasks();
    } catch (err) {
      console.log("Update error:", err.response?.data);
      alert("Failed to update task");
    }
  };

  // Toggle Completed 
  const toggleCompleted = async (task) => {
    try {
      await api.put(`/tasks/${task.id}`, {
        completed: !task.completed,
      });
      loadTasks();
    } catch (err) {
      console.log("Toggle error:", err.response?.data);
      alert("Failed to toggle");
    }
  };

  // Delete 
  const deleteTask = async (taskId) => {
    try {
      await api.delete(`/tasks/${taskId}`);
      loadTasks();
    } catch (err) {
      console.log("Delete error:", err.response?.data);
      alert("Failed to delete");
    }
  };

  //  UI 
  return (
    <div>
      <h2>{isAdmin ? "All Tasks (Admin)" : "Your Tasks"}</h2>

      <input
        placeholder="New Task"
        value={newTask}
        onChange={(e) => setNewTask(e.target.value)}
      />
      <button onClick={createTask}>Add Task</button>

      <ul>
        {tasks.map((task) => (
          <li key={task.id}>
            {editingTaskId === task.id ? (
              <>
                <input
                  value={editingTaskTitle}
                  onChange={(e) => setEditingTaskTitle(e.target.value)}
                />
                <input
                  value={editingTaskDescription}
                  onChange={(e) => setEditingTaskDescription(e.target.value)}
                />
                <label>
                  Done:
                  <input
                    type="checkbox"
                    checked={editingTaskCompleted}
                    onChange={(e) =>
                      setEditingTaskCompleted(e.target.checked)
                    }
                  />
                </label>

                <button onClick={updateTask}>Save</button>
                <button onClick={() => setEditingTaskId(null)}>Cancel</button>
              </>
            ) : (
              <>
                <span
                  style={{
                    textDecoration: task.completed
                      ? "line-through"
                      : "none",
                    cursor: "pointer",
                  }}
                  onClick={() => toggleCompleted(task)}
                >
                  {task.title}
                </span>{" "}
                - {task.description || "No description"}

                <button onClick={() => startEdit(task)}>Edit</button>
                <button onClick={() => deleteTask(task.id)}>Delete</button>
              </>
            )}
          </li>
        ))}
      </ul>

      <button onClick={onLogout}>Logout</button>
    </div>
  );
}
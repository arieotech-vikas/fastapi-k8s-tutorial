import { useEffect, useState } from "react";

interface Task {
  id: number;
  title: string;
  done: boolean;
}

function App() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [newTitle, setNewTitle] = useState("");

  const fetchTasks = () => {
    fetch(`/tasks`)
      .then((res) => res.json())
      .then((data) => setTasks(data.tasks));
  };

  useEffect(() => {
    fetchTasks();
  }, []);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTitle.trim()) return;

    fetch(`/tasks?title=${encodeURIComponent(newTitle)}`, {
      method: "POST",
    }).then(() => {
      setNewTitle("");
      fetchTasks();
    });
  };

  return (
    <div>
      <h1>Tasks</h1>
      <form onSubmit={handleSubmit}>
        <input
          value={newTitle}
          onChange={(e) => setNewTitle(e.target.value)}
          placeholder="New task"
        />
        <button type="submit">Add</button>
      </form>
      <ul>
        {tasks.map((task) => (
          <li key={task.id}>{task.title}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;

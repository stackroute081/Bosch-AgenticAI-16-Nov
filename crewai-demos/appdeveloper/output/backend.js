const express = require('express');
const cors = require('cors');
const { v4: uuidv4 } = require('uuid');

const app = express();
const PORT = 3000;

// Middleware
app.use(cors());
app.use(express.json());

// In-memory storage
let tasks = [
    { id: '1', title: 'Learn Node.js', completed: false },
    { id: '2', title: 'Build a REST API', completed: true }
];

// Routes
// GET all tasks
app.get('/tasks', (req, res) => {
    res.status(200).json(tasks);
});

// POST a new task
app.post('/tasks', (req, res) => {
    const { title } = req.body;
    
    if (!title) {
        return res.status(400).json({ error: 'Title is required' });
    }

    const newTask = {
        id: Date.now().toString(), // Simple ID generation
        title,
        completed: false
    };

    tasks.push(newTask);
    res.status(201).json(newTask);
});

// DELETE a task
app.delete('/tasks/:id', (req, res) => {
    const { id } = req.params;
    const initialLength = tasks.length;
    
    tasks = tasks.filter(task => task.id !== id);

    if (tasks.length === initialLength) {
        return res.status(404).json({ error: 'Task not found' });
    }

    res.status(200).json({ message: 'Task deleted successfully' });
});

// Server Startup
app.listen(PORT, () => {
    console.log(`Task Management API running at http://localhost:${PORT}`);
});
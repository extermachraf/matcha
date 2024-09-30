const express = require('express');
const router = express.Router();
const connectDb = require('../db'); // Adjust path as needed

let db;

// Initialize DB before route is accessed
const initializeDb = async () => {
  if (!db) {
    db = await connectDb(); // Await the database connection
  }
};

// GET all todos
router.get('/', async (req, res) => {
  try {
    await initializeDb(); // Ensure the database is connected
    const todos = await db.any('SELECT * FROM todo'); // Use 'any' method to fetch all todos
    res.json(todos);
  } catch (error) {
    console.error('Error fetching todos:', error.message);
    res.status(500).json({ error: error.message });
  }
});

// POST a new todo
router.post('/', async (req, res) => {
    const { description } = req.body;
    try {
      await initializeDb();
      const newTodo = await db.one(
        'INSERT INTO todo (description) VALUES ($1) RETURNING *',
        [description]
      );
      res.status(201).json(newTodo); // Respond with the created todo
    } catch (error) {
      console.error('Error creating todo:', error.message);
      res.status(500).json({ error: error.message });
    }
  });

// PUT (update) a todo by ID
router.put('/:id', async (req, res) => {
    const { id } = req.params;
    const { description } = req.body;
    try {
      await initializeDb();
      const updatedTodo = await db.one(
        'UPDATE todo SET description = $1 WHERE todo_id = $2 RETURNING *',
        [description, id]
      );
      res.json(updatedTodo); // Respond with the updated todo
    } catch (error) {
      console.error('Error updating todo:', error.message);
      res.status(500).json({ error: error.message });
    }
  });
// DELETE a todo by ID
router.delete('/:id', async (req, res) => {
    const { id } = req.params;
    try {
      await initializeDb();
      await db.none('DELETE FROM todo WHERE todo_id = $1', [id]);
      res.status(204).send(); // Respond with 204 No Content on success
    } catch (error) {
      console.error('Error deleting todo:', error.message);
      res.status(500).json({ error: error.message });
    }
  });

module.exports = router;

import { useState } from "@odoo/owl";

// Represents a single todo item
export class Todo {
    static nextId = 1;

    constructor(model, description) {
        this._model = model;
        this.id = Todo.nextId++;
        this.description = description;
        this.isCompleted = false;
    }

    toggle() {
        this.isCompleted = !this.isCompleted;
    }

    remove() {
        this._model.remove(this.id);
    }
}

// Manages a collection of Todo items
export class TodoModel {
    constructor() {
        this.todos = useState([]);
        this.nextId = 1;
    }

    // Create and add a new todo
    createTodo(description) {
        const desc = description.trim();
        if (desc) {
            const newTodo = new Todo(this, desc);
            newTodo.id = this.nextId++;
            this.todos.push(newTodo);
        }
    }

    // Add a new todo (alias for createTodo)
    add(description) {
        this.createTodo(description);
    }

    // Remove a todo by ID
    remove(id) {
        const index = this.todos.findIndex(todo => todo.id === id);
        if (index >= 0) {
            this.todos.splice(index, 1);
        }
    }

    // Load initial demo data
    load() {
        const initialTasks = [
            "Review documentation",
            "Complete tutorial exercise"
        ];
        initialTasks.forEach(task => this.createTodo(task));
        return Promise.resolve();
    }
}

import { useState } from "@odoo/owl";

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

export class TodoModel {
    constructor() {
        this.todos = useState([]);
    }

    createTodo(description) {
        if (description.trim()) {
            const todo = new Todo(this, description.trim());
            this.todos.push(todo);
        }
    }

    add(description) {
        this.createTodo(description);
    }

    remove(id) {
        const todoIndex = this.todos.findIndex((todo) => todo.id === id);
        if (todoIndex >= 0) {
            this.todos.splice(todoIndex, 1);
        }
    }

    load() {
        // Simulating initial data
        this.createTodo("Review documentation");
        this.createTodo("Complete tutorial exercise");
        return Promise.resolve();
    }
}
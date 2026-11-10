import { Component, useRef } from "@odoo/owl";

export class TodoModel {

    constructor() {
        this.todos = [];
    }

    findRealIndex(id) {
        return this.todos.findIndex((elem) => elem.id == id)
    }
    getTodos() {
        return this.todos;
    }
    getTodo(id) {
        id = this.findRealIndex(id)
        return this.todos[id];
    }
    addTodo(s) {
        this.todos.push(
            { id: this.todos.length === 0 ? 1 : this.todos[this.todos.length - 1].id + 1, description: s, isCompleted: false });

    }
    toggleState(todoId) {
        todoId = this.findRealIndex(todoId);
        this.todos[todoId].isCompleted = !this.todos[todoId].isCompleted;
    }
    removeTodos(todoId) {
        todoId = this.findRealIndex(todoId);
        this.todos.splice(todoId, 1);
    }
}

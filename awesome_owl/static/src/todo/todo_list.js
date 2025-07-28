import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutoFocus } from "../utils";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = { TodoItem };
    id = 1
    setup() {
        this.todos = useState([]);
        useAutoFocus();
    }

    addTodo(event) {
        const { target: { value }, keyCode } = event;
        if (!value.trim() || keyCode != 13) return;
        this.todos.push({
            id: this.id++,
            description: value,
            isCompleted: false,
        });
        event.target.value = '';
    }

    toggleState(todo_id) {
        const todo = this.todos.find((todo) => todo.id === todo_id);
        if (!todo) return;
        todo.isCompleted = !todo.isCompleted;
    }

    removeTodo(todo_id) {
        const todoIndex = this.todos.findIndex((todo) => todo.id === todo_id);
        if (todoIndex >= 0) {
            this.todos.splice(todoIndex, 1);
        }
    }
}
import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_items";
import { useAutoFocus } from "../utils";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = { TodoItem };
    setup() {
        useAutoFocus("todoInput");
        this.todos = useState([]);
        this.nextId = 1;
    }

    addTodo(event) {
        if (event.keyCode === 13) {
            const description = event.target.value.trim();
            if (description) {
                this.todos.push({
                    id: this.nextId++,
                    description: description,
                    isCompleted: false,
                });
                event.target.value = "";
            }
        }
    }

    toggleTodo(todoId) {
        const todo = this.todos.find(t => t.id === todoId);
        if (todo) {
            todo.isCompleted = !todo.isCompleted;
        }
    }

    removeTodo(todoId) {
        // Find the index of the todo to remove
        const index = this.todos.findIndex(t => t.id === todoId);
        if (index !== -1) {
            // Remove the todo from the array
            this.todos.splice(index, 1);
        }
    }
}
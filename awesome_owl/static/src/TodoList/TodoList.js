import { Component, useState } from "@odoo/owl";
import { TodoItem } from "../TodoItem/TodoItem";
import { useAutofocus } from "../utils";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";

    static components = { TodoItem };

    static props = {};

    setup() {
        this.todos = useState([]);
        this.todoInputRef = useAutofocus("todoInput");
    }

    addTodo(ev) {
        if (ev.key === "Enter" && ev.target.value.trim() !== "") {
            const newTodoItem = {
                id: this.todos.length + 1,
                description: ev.target.value.trim(),
                isComplete: false,
            };
            this.todos.push(newTodoItem);
            ev.target.value = "";
        }
    }

    toggleTodo(todoId) {
        const todo = this.todos.find(t => t.id === todoId);
        if (todo) {
            todo.isComplete = !todo.isComplete;
        }
    }

    removeItem(todoId) {
        const index = this.todos.findIndex(t => t.id === todoId);
        if (index !== -1) {
            this.todos.splice(index, 1);
        }
    }
}

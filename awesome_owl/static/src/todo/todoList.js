import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { TodoItem } from "./todoItem";
import { useAutofocus } from "../utils/useAutofocus";

export class TodoList extends Component {
    static template = "awesome_owl.todoList";
    static components = { TodoItem };

    setup() {
        this.nextId = 1
        this.todos = useState([]);
        this.inputRef = useAutofocus('todo_input');
    }

    addTodo(ev) {
        if (ev.keyCode === 13 && ev.target.value.trim() !== "") {
            this.todos.push({
                id: this.nextId++,
                description: ev.target.value,
                isCompleted: false,
            });
            ev.target.value = "";
        }
    }

    toggleTodo = (todoId) => {
        const todo = this.todos.find((t) => t.id === todoId);
        if (todo) {
            todo.isCompleted = !todo.isCompleted;
        }
    }

    removeTodo = (todoId) => {
    const index = this.todos.findIndex((t) => t.id === todoId);
    if (index >= 0) {
        this.todos.splice(index, 1);
    }
    }
}

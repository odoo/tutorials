import {Component, useState} from "@odoo/owl";
import {useAutofocus} from "../utils";
import {TodoItem} from "./todo";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = {TodoItem};
    static props = {};

    setup() {
        this.nextId = 1;
        this.todos = useState([]);
        this.state = useState({inputValue: ""});

        this.inputRef = useAutofocus("todo_input");

        this.toggleTodo = this.toggleTodo.bind(this);
        this.removeTodo = this.removeTodo.bind(this);
    }

    addTodo(ev) {
        if (ev.keyCode === 13 && this.state.inputValue.trim() !== "") {
            this.todos.push({
                id: this.nextId++,
                description: this.state.inputValue.trim(),
                isCompleted: false,
            });
            this.state.inputValue = "";
        }
    }

    toggleTodo(todoId) {
        const todo = this.todos.find((t) => t.id === todoId);
        if (todo) {
            todo.isCompleted = !todo.isCompleted;
        }
    }

    removeTodo(todoId) {
        const index = this.todos.findIndex((t) => t.id === todoId);
        if (index >= 0) {
            this.todos.splice(index, 1);
        }
    }

    clear() {
        this.todos.splice(0);
    }
}

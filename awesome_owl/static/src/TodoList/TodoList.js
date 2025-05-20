import { Component, useState, useRef } from "@odoo/owl";
import { TodoItem } from "./TodoItem";
import { useAutofocus } from "../utils";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = { TodoItem };

    setup() {
        this.todos = useState([]);
        this.state = useState({ counter: 0 });

        this.inputRef = useRef('todo_input');

        useAutofocus(this.inputRef);
    }

    addTodo(ev) {
        if (ev.keyCode === 13 && ev.target.value) {
            this.todos.push({ id: this.state.counter, description: ev.target.value, isCompleted: false });
            this.state.counter += 1;
            ev.target.value = "";
        }
    }

    toggleTodoState(todoId) {
        const todo = this.todos.find(todo => todo.id === todoId);
        if (todo)
            todo.isCompleted = !todo.isCompleted;
    }

    removeTodoItem(todoId) {
        const todoIndex = this.todos.findIndex((todo) => todo.id === todoId);
        if (todoIndex >= 0)
            this.todos.splice(todoIndex, 1);
    }
}

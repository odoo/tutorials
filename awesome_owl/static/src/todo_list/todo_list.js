import { Component, useState } from "@odoo/owl";
import { useAutoFocus } from '../utils';
import { TodoItem } from "./todo_item";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = { TodoItem };

    setup() {
        this.input = useState({ counter: 0, value: "" });
        this.todos = useState([]);

        this.inputRef = useAutoFocus("todo_input");
        this.toggleState = this.toggleState.bind(this);
        this.removeTodo = this.removeTodo.bind(this);
    }

    addTodo(ev) {
        if (ev.keyCode !== 13 || this.input.value.length === 0) return;
        this.todos.push({ id: this.input.counter++, description: this.input.value, isCompleted: false });
        this.input.value = "";
    }

    toggleState(id) {
        this.todos.filter((todo) => todo.id === id).forEach((todo) => todo.isCompleted = !todo.isCompleted);
    }

    removeTodo(id) {
        const index = this.todos.findIndex((todo) => todo.id === id);
        if (index >= 0) this.todos.splice(index, 1);
    }
}

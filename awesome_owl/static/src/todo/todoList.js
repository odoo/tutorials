import { Component, useState, useRef, onMounted } from "@odoo/owl"
import { TodoItem } from "./todoItem";
import { useAutofocus } from "../utils";

export class TodoList extends Component {
    static template = 'awesome_owl.todoList';
    static components = { TodoItem };

    setup() {
        this.todos = useState([]);
        this.id = 1;

        this.inputRef = useAutofocus('todo');
    }

    addTodo(ev) {
        if (ev.keyCode !== 13)
            return;

        const value = ev.target.value.trim();

        if (value.length === 0)
            return;

        this.todos.push({id: this.id++, description: value, isCompleted: false});

        ev.target.value = "";
    }
}

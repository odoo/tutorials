import { Component, useRef, useState, onMounted } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutofocus } from "../utils";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = { TodoItem };

    setup() {
        this.todos = useState([]);
        this.todo_idx = useState({ value: 1 });
        useAutofocus("todo_input");
    }

    addTodo(ev) {
        if (ev.keyCode !== 13 || ev.target.value == "") {
            return;
        }
        this.todos.push({ "id": this.todo_idx.value++, "description": ev.target.value, "isCompleted": false });
        ev.target.value = "";
    }

    toggleTodo(id) {
        const todo = this.todos.find((todo) => todo.id === id);
        todo.isCompleted = !todo.isCompleted;
    }
}

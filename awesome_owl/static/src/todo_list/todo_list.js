import {Component, useState} from "@odoo/owl";
import {TodoItem} from "./todo_item";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = {TodoItem};

    setup() {
        this.todos = useState([]);
    }

    addTodo(ev) {
        if (ev.keyCode === 13 && ev.target.value.trim() != "") {
            const newTodo = {
                id: this.todos.length + 1,
                description: ev.target.value.trim(),
                isCompleted: false,
            };
            this.todos.push(newTodo);
            ev.target.value = "";
        }
    }
}
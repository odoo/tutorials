import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = { TodoItem };

    setup() {
        this.todos = useState([]);
        this.todo_idx = useState({ value: 1 });
    }

    addTodo(ev) {
        if (ev.keyCode !== 13 || ev.target.value == "") {
            return;
        }
        this.todos.push({ "id": this.todo_idx.value++, "description": ev.target.value, "isCompleted": false });
        ev.target.value = "";
    }
}

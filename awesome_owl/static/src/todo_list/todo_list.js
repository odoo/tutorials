import {Component, useState} from "@odoo/owl";
import {TodoItem} from "./todo";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = {TodoItem};

    setup() {
        this.nextId = 1;
        this.todos = useState([]);
    }

    addTodo(ev) {
        if (ev.keyCode === 13 && ev.target.value.trim() !== "") {
            this.todos.push({
                id: this.nextId++,
                description: ev.target.value.trim(),
                isCompleted: false
            });
            ev.target.value = "";
        }
    }

     
}

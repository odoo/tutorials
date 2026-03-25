import {Component, useState} from "@odoo/owl";
import {TodoItem} from "./todo_item";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = {TodoItem};
    static props = {};

    setup() {
        this.todos = useState([]);
        this.nextId = 1;
    };

    addTodo(ev) {
        if ((ev.keyCode === 13) && (ev.target.value.length > 0)) {
            this.todos.push({id: this.nextId, description: ev.target.value, isCompleted: false});
            this.nextId++;
            ev.target.value = "";
        }
    }
}

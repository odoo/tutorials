import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item"

var id = 1

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";

    static components = { TodoItem };
    
    setup() {
        this.state = useState([]);
    }

    addTodo(ev) {
        if (ev.keyCode === 13 && ev.target.value !== "") {
            this.state.push({id: id, description: ev.target.value, isCompleted: false});
            id++;
            ev.target.value = "";
        }
    }
}

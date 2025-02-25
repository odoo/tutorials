import { Component, useState } from "@odoo/owl";
import {ToDoItem}  from "./todoitem";

export class ToDoList extends Component {
    static template = "awesome_owl.ToDoList";
    static components = { ToDoItem };

    setup() {
        this.ids = 1;
        this.todos = useState([]);
    }

    addTodo(ev) {
        if(ev.keyCode === 13 && ev.target.value != ''){
            this.todos.push({
                id: this.ids++,
                description: ev.target.value,
                isCompleted: false,
            });
            ev.target.value = "";
        }
    }
}
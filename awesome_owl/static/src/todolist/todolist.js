/** @odoo-module **/

import { useState, Component } from "@odoo/owl";

import { TodoItem } from "./todoitem";

export class TodoList extends Component {
    static template = "awesome_owl.todolist";
    static components = { TodoItem };
    
    todos = useState([]);
    state = useState({ counter: 0 });

    addTodo(event) {
        if (event.keyCode === 13 && event.target.value !== "") {
            console.log(event);
            this.todos.push({
                id: this.state.counter,
                description: event.target.value,
                isCompleted: false,
            });
            this.state.counter++;
        }
    }
}

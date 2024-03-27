/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { Autofocus } from "../utils"

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = { TodoItem }

    setup() {

        

        this.todos = useState([]);

        let todoList = this.todos;
        this.deleteTodoItem = (id) => {
            let idx = todoList.findIndex(o => o.id === id);
            if (idx >= 0) {
                todoList.splice(idx, 1);
            }
        }

        this.todos.push({id: 1, description: "Eat 5 fruits and vegetables a day", isCompleted: false, delete: this.deleteTodoItem});
        this.todos.push({id: 2, description: "Pet a unicorn", isCompleted: false, delete: this.deleteTodoItem});
        this.todos.push({id: 3, description: "Vainquish thy enemies", isCompleted: false, delete: this.deleteTodoItem});
        this.todos.push({id: 4, description: "Turn on the computer", isCompleted: true, delete: this.deleteTodoItem});

        this.nextId = this.todos.length + 1;

        Autofocus("focus")
    }

    addTodo(ev) {
        // If enter key is pressed
        if (ev.keyCode === 13) {
            let newval = ev.target.value;
            if (newval.length !== 0) {
                this.todos.push({id: this.nextId, description: newval, isCompleted: false, delete: this.deleteTodoItem });
                this.nextId++;
            }
        }
    }

}

/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutofocus } from "./utils";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = {TodoItem};

    setup() {
        this.todos = useState([
            { id: 1, description: "buy milk", isCompleted: false },
            { id: 2, description: "buy bread", isCompleted: true },
            { id: 3, description: "buy freedom", isCompleted: false },
        ]);
        this.state = { text: "" };
        useAutofocus("todos_input");
    }

    addTodo(ev){
        if (ev.keyCode === 13 && this.state.text != "") {
            this.todos.push({ id: this.todos[this.todos.length-1].id + 1, description: this.state.text, isCompleted: false });
        }
    }

    removeTodoWithId(todo_id) {
        const index = this.todos.findIndex((elem) => elem.id === todo_id);
        if (index >= 0) {
            this.todos.splice(index, 1);
            for (let i=0;i<this.todos.length;i++) {
                this.todos[i].id = i+1;
            }
        }
    }
}

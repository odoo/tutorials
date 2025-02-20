/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { useAutofocus } from "../utils";
import { TodoItem } from "./todo_item";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = { TodoItem };

    static props = {}

    setup() {
        this.NextId = 1;
        this.Todos = useState([]);
        useAutofocus('input');
    }

    addTodo(e) {
        let value = document.getElementById('mytodo').value;
        if ((e.keyCode === 13 || e.type === "click") && value) {
            this.Todos.push({
                id: this.NextId++,
                description: value,
                isCompleted: false
            });
            setTimeout(() => {
                window.scrollTo({top: document.body.scrollHeight, behavior: "smooth"});
            }, 0);
        }
    }

    ToggleStatus(todo){
        if (todo) {
            todo.isCompleted = !todo.isCompleted;
        }
    }

    RemoveTodo(id){
        const index = this.Todos.findIndex((elem) => elem.id === id);
        this.Todos.splice(index, 1);
    }
}

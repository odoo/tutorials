/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item/todo_item";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";

    static components = {
        TodoItem,
    };

    setup() {
        this.todos = useState([]);
    }

    static props = {
        todos: {
            type: Array,
            optional: true,
            default: () => [],
        },
    };

    addTodo(ev){
        let input_val = ev.target.value;
        if (ev.keyCode === 13 && input_val != "") {
            this.todos.push({
                id: this.todos.length + 1,
                description: input_val,
                isCompleted: false,
            });
            ev.target.value = "";
        }
    }
}

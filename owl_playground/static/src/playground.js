/** @odoo-module **/

import { useRef, useState, Component } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { TodoList } from "./todo/todo";

export class Playground extends Component {
    static template = "owl_playground.playground";
    static components = { Counter, TodoList };

    setup() {
        this.todos = useState(
            [
                { id: 1, description: "buy milk", done: false },
                { id: 2, description: "buy eggs", done: true },
                { id: 3, description: "buy avocado", done: true },
            ]
        );
    }

    addTodo(e) {
        if (e.keyCode === 13 && e.target.value) {
            this.todos.push(
                {
                    id: this.todos.length + 1,
                    description: e.target.value,
                    done: false
                }
            );
            e.target.value = "";
        }
    }
}

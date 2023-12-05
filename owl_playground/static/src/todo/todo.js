/** @odoo-module **/

import { useRef, Component } from "@odoo/owl"

export class Todo extends Component {
    static template = "todo.todo";

    static props = {
        id: Number,
        description: String,
        done: Boolean
    }
}

export class TodoList extends Component {
    static template = "todo.todolist";
    static components = { Todo };
}

/** @odoo-module **/

import { Component } from "@odoo/owl";

export class Todo extends Component {
    toggleDone() {
        this.props.toggleDone(this.props.id)
    }

    removeTodo() {
        this.props.removeTodo(this.props.id)
    }
}

Todo.props = {
    id: { type: Number },
    description: { type: String },
    done: { type: Boolean },
    toggleDone: { type: Function },
    removeTodo: { type: Function },
}

Todo.template = "owl_playground.todo"

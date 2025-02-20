/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.TodoItem";

    static props = {
        Todos: {
            type: Object,
            required: false
        },
        ToggleStatus: Function,
        RemoveTodo: Function,
    }

    OnToggleStatus() {
        this.props.ToggleStatus(this.props.Todos);
    }

    OnRemoveTodo() {
        this.props.RemoveTodo(this.props.Todos.id);
    }
}

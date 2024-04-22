/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.todo_item";
    static props = {
        todo: { id: Number, description: String, isCompleted: Boolean },
        toggleState: {type: Function},
        removeTodo: {type: Function},
       };

        change() {
            this.props.toggleState(this.props.todo.id)
        }

        delete() {
            this.props.removeTodo(this.props.todo.id)
        }
}
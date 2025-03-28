/** @odoo-module **/

import { Component } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.todo_item";

    static props = {
        todo: {
            type: Object,
            values: { id: Number,description: String, isCompleted: Boolean}
        },
        toggleState: Function,
        removeTodo: Function
    };

    confirm_todo(event) {
        console.log("Toggle : " + this.props.todo.id);
        this.props.toggleState(this.props.todo.id);
    }

    remove_todo(event) {
        console.log("Delete : " + this.props.todo.id);
        this.props.removeTodo(this.props.todo.id);
    }
}

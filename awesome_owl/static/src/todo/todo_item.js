/** @odoo-module **/

import { Component } from "@odoo/owl";

export class TodoItem extends Component {

    static template = "awesome_owl.Todo_item"

    static props = {
        todo: {
            type: Object,
            values: {id: Number, description: String, isCompleted: Boolean},
        },
        onCheck: {
            type: Function,
            optional: true
        },
        rmTodo: {
            type: Function,
            optional: true
        }
    };

    toggleCheckBox() {
        this.props.onCheck(this.props.todo.id);
    };

    removeTodo() {
        this.props.rmTodo(this.props.todo.id);
    }
}

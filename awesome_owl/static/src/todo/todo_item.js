/** @odoo-module **/

import { Component} from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.todo_item";

    static props = {
        todo: {
            type: Object,
            shape: {
                id: { type: Number },
                description: { type: String },
                isCompleted: { type: Boolean },
            },
        },
        toggleTodo: { type: Function },
    }

    onChange() {
        this.props.toggleTodo(this.props.todo.id);
    }
}
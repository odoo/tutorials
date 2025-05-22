/** @odoo-module **/
import { Component } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.TodoItem";
    static props = {
        todo: {
            type: Object,
            shape: {
                id: Number,
                description: String,
                isCompleted: Boolean,
            },
            required: true,
        },
        toggleState: { type: Function },
        removeState: { type: Function }
    };

    toggle() {
        this.props.toggleState(this.props.todo.id);
    }
    
    remove() {
        this.props.removeState(this.props.todo.id);
    }
}

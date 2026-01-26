import { Component, useState } from "@odoo/owl";


export class TodoItem extends Component {
    static template = "awesome_owl.TodoItem";

    static props = {
        todo: {
            type: Object,
            shape: {
                id: { type: Number },
                description: { type: String },
                isCompleted: { type: Boolean },
            }
        },
        toggleState: {
            type: Function,
            optional: true,
        },
        removeTodo: {
            type: Function,
            optional: true,
        }
    };

    change() {
        if (this.props.toggleState) {
            this.props.toggleState(this.props.todo.id);
        }
    };

    remove() {
        if (this.props.removeTodo) {
            this.props.removeTodo(this.props.todo.id);
        }
    };
}

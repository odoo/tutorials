import { Component, useState } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.todoitem";
    static props = {
        todo: {
            type: Object,
            shape: {
                id: Number,
                description: String,
                isCompleted: Boolean,
            },
        },
        toggleState: {
            type: Function,
        },
        removeTodo: {
            type: Function,
        },
    };

    change(event) {
        let isCompleted = event.target.checked;
        this.props.toggleState(this.props.todo.id, isCompleted);
    }

    remove() {
        this.props.removeTodo(this.props.todo.id);
    }
}
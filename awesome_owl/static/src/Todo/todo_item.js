/** @odoo-module */

import { Component } from '@odoo/owl';

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
        },
        removeTodo: { type: Function },
    };

    get todoClasses() {
        return this.props.todo.isCompleted ? 'text-muted text-decoration-line-through' : '';
    }

    toggleTodo() {
        this.props.todo.isCompleted = !this.props.todo.isCompleted
    }
    deleteTodo() {
        this.props.removeTodo(this.props.todo.id);
    }
}

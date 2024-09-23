/** @odoo-module */

import {Component, useState} from '@odoo/owl'

export class TodoItem extends Component {
    static template = "awesome_owl.todo.todo_item"
    static props = {
        onDeleteClicked: {
            type: Function,
        },
        todo : {
            type: Object,
        }
    }

    onDeleteClicked() {
        this.props.onDeleteClicked(this.props.todo.id);
    }

    onToggleDone() {
        this.props.todo.done = !this.props.todo.done;
        if (this.props.todo.done) {
            this.props.todo.dateCompleted = new Date().getTime();
        } else {
            this.props.todo.dateCompleted = null;
        }
    }

    get formattedDateAdded() {
        const date = new Date(this.props.todo.dateAdded);
        return date.toLocaleString();
    }

    get formattedDateCompleted() {
        if (!this.props.todo.dateCompleted) {
            return "";
        }
        const date = new Date(this.props.todo.dateCompleted);
        return date.toLocaleString();
    }
}
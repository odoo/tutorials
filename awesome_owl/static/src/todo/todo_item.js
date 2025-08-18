import { Component, useState } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.TodoItem";
    static props = {
        todo: {
            type: Object,
            shape: {
                id: Number,
                description: String,
                isCompleted: Boolean,
            }
        },
        toggleTaskState: {
            type: Function,
        },
        taskDelete: {
            type: Function,
        }

    }

    toggleTaskState() {
        this.props.toggleTaskState(this.props.todo.id);
    }

    taskDelete() {
        this.props.taskDelete(this.props.todo.id);
    }
}

import { Component, xml, useState } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.todo_item";
    static props = {
        item: {type: Object, shape: {
            id: {type: Number},
            description: {type: String},
            isCompleted: {type: Boolean, optional: true}
        }},
        toggleState: {type: Function},
        removeTodo: {type: Function},
    };

    setup() {
        this.markCompleted = this.markCompleted.bind(this);
        this.deleteTask = this.deleteTask.bind(this);
    }

    markCompleted() {
        this.props.toggleState(this.props.item.id);
    }

    deleteTask() {
        this.props.removeTodo(this.props.item.id);
    }
}


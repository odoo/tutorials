import { Component, useState } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.todo_item"

    static props = {
        id: { type: Number },
        description: { type: String, optional: true },
        isCompleted: { type: Boolean, optional: true },
        toggleState: { type: Function, optional: true },
        removeTodo: { type: Function, optional: true }
    }

    setup() {
        //this.id = this.props.id;
        //this.description = useState({ value: this.props.description != null ? this.props.description  : 'No description' });
        //this.isCompleted = useState({ value: this.props.isCompleted != null ? this.props.isCompleted : false });
    }
}
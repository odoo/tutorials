import { Component, useState } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.todo_item";
    static props = {
        id: { type: Number },
        description: { type: String },
        isCompleted: { type: Boolean }
    };

    onChange() {
        this.state.isCompleted = !this.state.isCompleted;
    }

    setup() {
        this.state = useState({
            isCompleted: this.props.isCompleted
        })
    }

};

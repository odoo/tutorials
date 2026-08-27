import { Component, useState} from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.todo_item";

    static props = {
        id: Number,
        description: String,
        isCompleted: Boolean,
        toggleState: Function,
        onRemove: Function
    };

    toggleTodo() {
        if (this.props.toggleState) {
            this.props.toggleState(this.props.id)
        }
    }

    removeTodo() {
        if (this.props.onRemove) {
            this.props.onRemove(this.props.id)
        }
    }
}

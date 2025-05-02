import { Component } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.todoitem";
    static props = {
        todo: {
            id: Number,
            description: String,
            isCompleted: Boolean,
        },
        onRemove: Function,
    };

    toggleState() {
        this.props.todo.isCompleted = !this.props.todo.isCompleted;
    }

    onClick() {
        this.props.onRemove(this.props.todo.id);
    }
}

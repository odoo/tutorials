import { Component } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.todo_item";
    static props = {
        id: Number,
        description: String,
        isCompleted: Boolean,
        toggleCompleted: Function,
        removeTodo: Function,
    };

    toggleCompleted() {
        this.props.toggleCompleted(this.props.id);
    }

    removeTodo() {
        this.props.removeTodo(this.props.id);
    }
}

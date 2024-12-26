import { Component } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.TodoItem";
    static props = {
        id: Number,
        description: String,
        isCompleted: Boolean,
        toggleState: Function,
        removeTodo: Function
    }

    onCheck() {
        this.props.toggleState(this.props.id);
    }

    onRemove() {
        this.props.removeTodo(this.props.id);
    }
}

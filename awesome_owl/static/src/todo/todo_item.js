import { Component } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.TodoItem";
    static props = {
        todo: {
            type: Object,
            shape: { id: Number, description: String, isCompleted: Boolean },
        },
        toggleState: Function,
        removeTodo: Function,
    };

    togglerAction() {
        this.props.toggleState(this.props.todo.id);
    }

    removeAction() {
        this.props.removeTodo(this.props.todo.id);
    }
}

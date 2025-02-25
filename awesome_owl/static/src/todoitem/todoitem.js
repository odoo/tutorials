import { Component } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.TodoItem";
    static props = {
        todo: {
            type: Object,
            shape: { id: Number, description: String, isCompleted: Boolean }
        },
        toggleState: Function,
        removeTodo: Function,
    };

    onToggle() {
        this.props.toggleState(this.props.todo);
    }

    onRemove() {
        this.props.removeTodo(this.props.todo);
    }

}

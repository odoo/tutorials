import { Component } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.todoitem";
    static props = {
        todo: {
            Object,
            shape: { id: Number, description: String, isCompleted: Boolean }
        },
        toggleState: Function,
        removeTodo: Function,
    };

    handleToggle() {
        this.props.toggleState(this.props.todo.id);
    }

    handleRemove() {
        this.props.removeTodo(this.props.todo.id);
    }
}

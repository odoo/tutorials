import { Component } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.todo_item";

    static props = {
        todo: {
            type: Object,
            shape: {
                id: { type: Number },
                description: { type: String },
                isCompleted: { type: Boolean },
            },
        },
        onToggle: { type: Function, optional: true },
        removeTodo: { type: Function, optional: true },
    };

    toggleComplete() {
        this.props.todo.isCompleted = !this.props.todo.isCompleted;
        if (this.props.onToggle) {
            this.props.onToggle(this.props.todo);
        }
    }

    handleRemove() {
        if (this.props.removeTodo) {
            this.props.removeTodo(this.props.todo)
        }
    }
}

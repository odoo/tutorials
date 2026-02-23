import { Component } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.TodoItem";

    static props = {
        // Define a shape for the todo object
        todo: {
            type: Object,
            shape: {
                id: { type: [String, Number], required: true },
                description: { type: String, required: true },
                isCompleted: { type: Boolean, required: true },
            },
            required: true,
        },
        toggleState: { type: Function, required: true },
        removeTodo: { type: Function, required: true },
    };

    onCheckboxChange() {
        // Call parent callback with the todo ID
        this.props.toggleState(this.props.todo.id);
    }

    onRemoveClick() {
        this.props.removeTodo(this.props.todo.id);
    }
}
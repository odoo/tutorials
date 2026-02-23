import { Component } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.TodoItem";

    static props = {
        // Define a shape for the todo object
        todo: {
            type: Object,
            shape: {
                id: { type: [String, Number], optional: true },
                description: { type: String, optional: true },
                isCompleted: { type: Boolean, optional: true },
            },
            optional: true,
        },
        toggleState: { type: Function, optional: true },
        removeTodo: { type: Function, optional: true },
    };

    onCheckboxChange() {
        // Call parent callback with the todo ID
        this.props.toggleState(this.props.todo.id);
    }

    onRemoveClick() {
        this.props.removeTodo(this.props.todo.id);
    }
}
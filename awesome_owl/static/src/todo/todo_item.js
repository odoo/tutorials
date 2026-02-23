import { Component } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.TodoItem";

    static props = {
        // Define a shape for the todo object
        todo: {
            shape: {
                id:  [String, Number],
                description:  String,
                isCompleted: Boolean, 
            },
        },
        toggleState:  Function, 
        removeTodo: Function,
    };

    onCheckboxChange() {
        // Call parent callback with the todo ID
        this.props.toggleState(this.props.todo.id);
    }

    onRemoveClick() {
        this.props.removeTodo(this.props.todo.id);
    }
}
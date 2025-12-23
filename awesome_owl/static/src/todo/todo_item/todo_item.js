import { Component } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.todo.todo_item";

    static props = {
        todo: {
            type: Object,
            shape: {
                id: Number,
                description: String,
                isCompleted: Boolean,
            }
        },
        toggleState: {type: Function},
        removeTodo: {type: Function},
    };

    toggleState() {
        this.props.toggleState(this.props.todo.id);
    }

    removeTodo() {
        this.props.removeTodo(this.props.todo.id);
    }
}

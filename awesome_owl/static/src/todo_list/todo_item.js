import { Component } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.TodoItem";
    static props = {
        todo: {
            type: Object,
            shape: {
                id: Number,
                description: String,
                isCompleted: Boolean,
            }
        },
        toggleState: Function,
        removeTodo: Function,
    };

    onChange() {
        const { toggleState, todo } = this.props;
        toggleState(todo.id);
    }

    onClick() {
        const { removeTodo, todo } = this.props;
        removeTodo(todo.id);
    }
}

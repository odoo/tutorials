import { Component } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.todo_item";

    static props = {
        todo: {
            type: Object,
            shape: {
                id: Number,
                description: String,
                isCompleted: Boolean,
            }
        },
        toggleState: { type: Function },
        removeTodo: { type: Function }
    }
    toggle() {
        this.props.toggleState(this.props.todo.id);
    }
    deleteTodo() {
        this.props.removeTodo(this.props.todo.id);
    }
}

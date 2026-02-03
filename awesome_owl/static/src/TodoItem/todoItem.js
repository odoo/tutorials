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
            },
        },
        Change: { type: Function, optional: true },
        removeTodo: { type: Function, optional: true },
    };

    toggleState(ev) {
        this.props.Change?.(ev.target.value);
    }

    removeTodo(ev) {
        this.props.removeTodo?.(ev.target.dataset.id);
    }
}

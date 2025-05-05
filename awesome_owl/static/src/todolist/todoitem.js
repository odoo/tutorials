import { Component } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.todoitem";

    static props = {
        todo: {
            type: Object,
            shape: {
                id: Number,
                description: String,
                isCompleted: Boolean,
            },
        },
        removeTodo: { type: Function },
    };

    toggleState(ev) {
        if (!ev.target) {
            return;
        }

        this.props.todo.isCompleted = ev.target.checked;
    }
}

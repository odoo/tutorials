import { Component } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.TodoItem";

    static props = {
        todo: {
            type: Object,
            shape: { id: Number, description: String, isCompleted: Boolean },
        },
        toggleState: { type: Function, optional: true },
        deleteTodo: { type: Function, optional: true },
    };
}

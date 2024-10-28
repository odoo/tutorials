import { Component, useState } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.todo.item";
    static props = {
        todo: {
            type: Object,
            shape: {
                id: { type: Number },
                description: { type: String },
                isCompleted: { type: Boolean },
            },
        },
    };
}

export class TodoList extends Component {
    static template = "awesome_owl.todo.list";
    static components = { TodoItem };

    setup() {
        this.todos = useState([
            { id: 3, description: "buy milk", isCompleted: true },
            { id: 4, description: "buy butter", isCompleted: false },
        ]);
    }
}

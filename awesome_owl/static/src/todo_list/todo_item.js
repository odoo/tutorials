import { Component } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.TodoItem";
    static props = {
        todo: { type: Object,
            shape: {
                id: { type: Number, default: 0 },
                description: { type: String, default: "" },
                isCompleted: { type: Boolean, default: false },
            }
        }
    };
}
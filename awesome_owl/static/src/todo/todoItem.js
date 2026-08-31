import { Component, markup } from "@odoo/owl";
import { Counter } from "../counter/counter";

export class TodoItem extends Component {
    static template = "awesome_owl.todoItem";
    static components = { Counter };
    static props = {
        id: { type: Number },
        description: { type: String },
        isCompleted: { type: Boolean},
        toggleState: { type: Function, optional: true },
        removeTodo: { type: Function, optional: true },
    };

}

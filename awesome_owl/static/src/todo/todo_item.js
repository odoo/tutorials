import { Component } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.TodoItem";

    // Props validation
    static props = {
        todo: { type: Object, required: true },
    };
}
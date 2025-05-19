import { Component } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.todoitem";
    static props = {
        todo: {
            type: Object,
            validate: e => e.id >= 0,
        },
        toggleState: {
            type: Function,
        },
        removeTodo: {
            type: Function,
        },
    };
}

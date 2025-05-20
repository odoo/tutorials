import { Component } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.TodoItem"
    static props = {
        todo: { type: Object, optional: false },
        toggleState: { type: Function, optinal: false },
        removeTodo: { type: Function, optinal: false }
    };
}

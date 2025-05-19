import { Component } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.todoitem";
    static props = {
        todo: Object,
        onToggleState: Function,
        onRemoveTodo: Function,
    }
}

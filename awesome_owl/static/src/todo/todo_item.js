import { Component } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.todo_item";
    static props = {
        todo: { type: Object, optional: false },
        toggleState: { type: Function, optional: false },
        removeTodo: { type: Function, optional: false },
    };

    toggle() {
        this.props.toggleState(this.props.todo.id);
    }

    remove() {
        this.props.removeTodo(this.props.todo.id);
    }
}

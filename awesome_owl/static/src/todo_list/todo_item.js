import { Component } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.todo_item";

    static props = {
        todo: Object,
        toggleState: Function,
        removeTodo: Function,
    };

    toggleState() {
        this.props.toggleState(this.props.todo.id);
    }

    removeTodo() {
        this.props.removeTodo(this.props.todo.id);
    }
}

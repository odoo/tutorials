import { Component } from "@odoo/owl";
import { Todo } from "./todo";

export class TodoItem extends Component {
    static template = "awesome_owl.TodoItem";
    static props = {
        todo: Todo,
        toggleState: Function,
        removeTodo: Function,
    };

    onChange() {
        this.props.toggleState(this.props.todo.id);
    }

    onRemove() {
        this.props.removeTodo(this.props.todo.id);
    }
}

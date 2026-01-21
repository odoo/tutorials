import { Component } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.todo_item";

    toggle() {
        this.props.toggleState(this.props.todo.id);
    }

    remove(){
        this.props.removeTodo(this.props.todo.id);
    }
}

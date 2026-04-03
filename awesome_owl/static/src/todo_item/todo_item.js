import { Component } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.TodoItem";

    toggle() {
        this.props.toggleState(this.props.task.id);
    }

    remove() {
        this.props.deleteTask(this.props.task.id);
    }
}

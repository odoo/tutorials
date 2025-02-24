import { Component } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.todoitem"
    static props = {
        id: { type: Number },
        description: { type: String },
        isCompleted: { type: Boolean },
        toggleState: { type: Function },
        removeTodo: { type: Function }
    }
    onChange() {
        this.props.toggleState(this.props.id);
    }
    removeTodo() {
        this.props.removeTodo(this.props.id);
    }

}

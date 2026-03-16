import { Component } from "@odoo/owl";


export class TodoItem extends Component {
    static template = "awesome_owl.TodoItem";
    static props = {
        todo: Object,
        toggleState: { type: Function, optional: true },
        remove: { type: Function, optional: true },
    };

    toggleState() {
        this.props.todo.isCompleted = !this.props.todo.isCompleted;
    }

    removeTodo() {
        this.props.remove(this.props.todo.id);
    }

}

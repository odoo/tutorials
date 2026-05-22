import { Component } from "@odoo/owl";

export class TodoItem extends Component {    
    static template = "awesome_owl.TodoItem";
    static props = {
        todo: { type: Object },
        toggleStatus: Function,
        deleteTodo: Function,
    }

    callbackStatus() {
        this.props.toggleStatus(this.props.todo.id);
    }

    callbackDelete() {
        this.props.deleteTodo(this.props.todo.id);
    }
}

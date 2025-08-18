import { Component } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.todoitem";

    static props = {
        todo: Object,
        removeTodo: Function,
    };

    toggleTodo(event) {
        this.props.todo.isCompleted = event.target.checked;
    }

    removeTodo() {
        this.props.removeTodo(this.props.todo.id);
    }
}

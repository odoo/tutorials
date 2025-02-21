import { Component } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.TodoItem";
    static props = {
        todo: { type: Object, shape: { id: Number, description: String, isCompleted: Boolean }, required: true },
        removeTodo: Function,   
    };

    toggleTodo() {
        this.props.todo.isCompleted=!this.props.todo.isCompleted;
    }

    removeTodo() {
        this.props.removeTodo(this.props.todo.id); // ✅ Call removeTodo with the correct ID
    }
}

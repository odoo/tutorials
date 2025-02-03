import { Component, useState } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.todoitem";

    static props = {
        todo: Object,
        removeTodo: Function,
    }

    toggleTodo(event) {
        if (event.target.checked) {
            this.props.todo.isCompleted = true;
        } else {
            this.props.todo.isCompleted = false;
        }
    }

    removeTodo() {
        this.props.removeTodo(this.props.todo.id);
    }
}
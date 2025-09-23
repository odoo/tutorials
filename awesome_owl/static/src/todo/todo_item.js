import { Component, useState } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.todoItem";
    static props = { todo: Object, removeTodo: Function, toggle: Function };

    setup() {
        this.isCompleted = this.props.todo.isCompleted;
        this.toggle = this.toggle.bind(this);
    }

    toggle() {
        this.props.toggle(this.props.todo);
    }

    remove() {
        this.props.removeTodo(this.props.todo);
    }

}

import { Component, useState } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.todoitem";

    static props = {
        todo: Object,
        toggleState: Function,
        removeTodo: Function
    }

    setup() {
        this.toggleStateItem = this.toggleStateItem.bind(this)
        this.removeTodoItem = this.removeTodoItem.bind(this)
    }

    toggleStateItem() {
        this.props.toggleState(this.props.todo.id)
    }

    removeTodoItem() {
        this.props.removeTodo(this.props.todo.id)
    }
}

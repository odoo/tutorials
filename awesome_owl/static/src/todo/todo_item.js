import { Component } from "@odoo/owl"

export class TodoItem extends Component {
    static template = "awesome_owl.todo_item"

    static props = {
        todo: {type: Object},
        removeTodo: {type: Function},
    }

    toggleState() {
        this.props.todo.isCompleted = !this.props.todo.isCompleted
    }
}

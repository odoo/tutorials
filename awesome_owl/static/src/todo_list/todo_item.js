import { Component } from "@odoo/owl"

export class TodoItem extends Component {
    static template = "awesome_owl.todo_item"
    static props = {
        toggleState: Function,
        removeTodo: Function,
        todo: {
            type: Object,
            shape: {
                id: Number,
                description: String,
                isCompleted: Boolean
            }
        }
    }

    onTodoToggle() {
        this.props.toggleState(this.props.todo.id)
    }

    onRemoveTodo() {
        this.props.removeTodo(this.props.todo.id)
    }
}

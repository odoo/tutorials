import { Component } from "@odoo/owl"

export class TodoItem extends Component {
    static template = "awsome_owl.todo_item"

    static props = {
        deleteTodo: { type: Function },
        toggleState: { type: Function },
        todo: {
            type: Object,
            shape: {
                id: Number,
                description: String,
                isCompleted: Boolean
            }
        }
    }

    toggleState() {
        this.props.toggleState(this.props.todo.id);
    }


    removeTodo() {
        this.props.deleteTodo(this.props.todo.id)
    }
}

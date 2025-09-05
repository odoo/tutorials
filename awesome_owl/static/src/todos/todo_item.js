import { Component } from "@odoo/owl"

export class TodoItem extends Component {
    static template = "awesome_owl.todo_item"

    static props = {
        data: {
            id: { type: Number },
            description: { type: String },
            isCompleted: { type: Boolean }
        },
        toggleState: Function,
        removeTodo: Function,
    }

}

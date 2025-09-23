import { Component, useState } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.todo_item"
    static props = {
        id: String,
        todo: {type: {description: String, isCompleted: Boolean}},
        toggleState: Function 
    }

    setup() {
        this.id = this.props.id
        this.todo = useState(this.props.todo)
        this.toggleState = this.props.toggleState
    }
}

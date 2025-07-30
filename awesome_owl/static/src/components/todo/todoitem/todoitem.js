import { Component, useState } from "@odoo/owl"
import { Card } from "../../card/card"

export class TodoItem extends Component {
    static template = "awesome_owl.todoitem"
    static components = { Card }
    static props = {
        id: { type: Number },
        description: { type: String },
        isCompleted: { type: Boolean, default: false }
    }

    setup() {
        this.state = useState({
            todo: {
                id: String(this.props.id),
                description: this.props.description,
                isCompleted: this.props.isCompleted
            }
        })
    }
}

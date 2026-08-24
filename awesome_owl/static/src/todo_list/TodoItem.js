import { Component, useState} from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.todo_item";

    static props = {
        id: Number,
        description: String,
        isCompleted: Boolean,
    };

    setup() {
        this.state = useState({
            id: this.props.id,
            description: this.props.description,
            isCompleted: this.props.isCompleted
        })
    }
}

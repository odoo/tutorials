import { Component } from "@odoo/owl";


export class TodoItem extends Component {
    static template = "awesome_owl.todoitem";
    static props = {
        id: Number,
        description: String,
        isCompleted: Boolean,
        onToggle: {
            Function,
            optional: true,
        },
        onClick: {
          Function,
          optional: true,
        },
    };

    toggleState() {
        this.props.onToggle(this.props.id);
    }

    removeTodo() {
        this.props.onClick(this.props.id);
    }
}

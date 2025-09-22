import { Component } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.TodoItem";
    static props = {
        todo: {
            type: Object,
            shape: {
                id: Number,
                description: String,
                isCompleted: Boolean,
            },
        },
        toggleState: Function,
        delete: Function,
    };
    
    onChange() {
        if (this.props.toggleState) {
            this.props.toggleState(this.props.todo.id);
        }
    }

    onDelete() {
        this.props.delete(this.props.todo.id);
    }
}

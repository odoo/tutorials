import { Component } from "@odoo/owl";


export class TodoItem extends Component {
    static template = "awesome_owl.todo_item";
    static props = {
        todo: {
            type: Object,
            shape: {
                id: Number,
                description: String,
                isCompleted: Boolean,
            }
        },
        toggleState: {
            type: Function,
            optional: true
        },

        deleteTodo: {
            type: Function,
            optional: true
        }
    };

    onChange() {
        if (this.props.toggleState) {
            this.props.toggleState(this.props.todo.id);
        }
    }

    onRemove() {
        if (this.props.deleteTodo) {
            this.props.deleteTodo(this.props.todo.id)
        }
    }
}

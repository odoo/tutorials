import {Component} from "@odoo/owl";

export class TodoItem extends Component {
    static template = 'awesome_owl.todoitem';
    static props = {
        id: {
            type: Number
        },
        description: {
            type: String,
            optional: true
        },
        isCompleted: {
            type: Boolean
        },
        toggleState: {
            type: Function
        },
        deleteTodo: {
            type: Function
        }
    };

    onchange() {
        this.props.toggleState(this.props.id);
    };

    removeTodo() {
        this.props.deleteTodo(this.props.id);
    };
}

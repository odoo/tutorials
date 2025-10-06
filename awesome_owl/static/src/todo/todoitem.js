import { Component } from "@odoo/owl";

export class Todoitem extends Component {

    static template = "awesome_owl.Todoitem";
    static props = {
        todo: {

            type: Object,
            shape: {
                id: Number,
                description: String,
                isCompleted: Boolean
            }
        },
        toggleState: Function,
        removeTodo: Function
    };

    toggleTodo() {
        this.props.toggleState(this.props.todo);
    }

    remove() {
        this.props.removeTodo(this.props.todo);
    }
}

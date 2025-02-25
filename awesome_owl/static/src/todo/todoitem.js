import { Component } from "@odoo/owl";

export class TodoItem extends Component {
    static props = {
        todo: {
            type: Object,
            shape: {
                id: { type: Number } ,
                description: { type: String },
                isCompleted: { type: Boolean }
            }
        },
        removeTodo: { type: Function }
    }

    toggleState() {
        this.props.todo.isCompleted = !this.props.todo.isCompleted;
    }

    static template = "awesome_owl.todo.item";
}

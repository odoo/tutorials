import {Component} from "@odoo/owl"


export class TodoItem extends Component {
    static template = "awesome_owl.todo.item";

    static props = {
        id: Number,
        description: String,
        isCompleted: Boolean,
        toggleState: Function,
        deleteTodo: Function,
    }

    get id() {
        return this.props.id;
    }

    get description() {
        return this.props.description;
    }

    get isCompleted() {
        return this.props.isCompleted;
    }
}

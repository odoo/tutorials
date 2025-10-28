import {Component} from "@odoo/owl"


export class TodoItem extends Component {
    static template = "awesome_owl.todo.item";

    static props = {
        todo: {type: Object, shape: {id: Number, description: String, isCompleted: Boolean}},
        toggleState: {type: Function},
        deleteTodo: {type: Function},
    }

    get id() {
        return this.props.todo.id;
    }

    get description() {
        return this.props.todo.description;
    }

    get isCompleted() {
        return this.props.todo.isCompleted;
    }
}

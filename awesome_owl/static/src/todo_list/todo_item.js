import {Component} from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.todo_item"
    static Components
    static props = {
        todo: {type: Object, shape: {id: Number, description: String, isCompleted: Boolean}},
        toggleState: {type: Function, optional: true},
        onRemoveTodo: {type: Function, optional: true},
    }

    onCheckToggle() {
        if (this.props.toggleState) {
            this.props.toggleState();
        }
    }

    onRemoveTodo() {
        if (this.props.onRemoveTodo) {
            this.props.onRemoveTodo();
        }
    }

}

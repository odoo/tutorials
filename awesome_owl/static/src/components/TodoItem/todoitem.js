import { Component} from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.todoitem";
    static props = {
        todo: { type: Object },
        toggleState: {type: Function},
        removeTodo: {type: Function}
    };

    toggleState() {
        this.props.toggleState(this.props.todo.id);
    }

    removeTodo() {
        this.props.removeTodo(this.props.todo.id);
    }

}

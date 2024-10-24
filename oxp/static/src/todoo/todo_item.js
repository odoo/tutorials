/** @odoo-module **/
import {Component} from "@odoo/owl";

export class TodoItem extends Component {
    static template = "oxp.TodoItem";
    static props = {
        todo: {
            type: Object,
            shape: {id: Number, desc: String, isDone: Boolean},
        },
        toggle: Function,
        remove: Function,
    };

    onChange() {
        this.props.toggle(this.props.todo.id);
    }

    remove() {
        this.props.remove(this.props.todo.id);
    }

}

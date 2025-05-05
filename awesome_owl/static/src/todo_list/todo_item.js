import { Component } from "@odoo/owl";
import { Todo } from "./todo";

export class TodoItem extends Component {
    static template = "awesome_owl.todo_item";
    static props = {
        todo: Todo,
        remove: { type: Function },
    };

    onClick() {
        if (this.props.remove) {
            this.props.remove(this.props.todo.id);
        }
    }
}

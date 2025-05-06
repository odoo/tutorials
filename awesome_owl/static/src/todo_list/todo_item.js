import { Component } from "@odoo/owl";
import { Todo } from "./todo";

export class TodoItem extends Component {
    static template = "awesome_owl.TodoItem";
    static props = {
        todo: Todo,
        remove: { type: Function },
    };

    removeItem() {
        if (this.props.remove) {
            this.props.remove(this.props.todo.id);
        }
    }
}

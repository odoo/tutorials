import { Component } from "@odoo/owl";
import { TodoModel } from "./todo_model";

export class TodoItem extends Component {
    static template = "awesome_owl.TodoItem";
    static props = {
        model: TodoModel,
        id: Number,
    };

    onChange() {
        this.props.model.toggle(this.props.id);
    }

    onRemove() {
        this.props.model.remove(this.props.id);
    }
}

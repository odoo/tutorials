import { Component } from "@odoo/owl";
import { Todo } from "./todo";
import { Card } from "../card/card";

export class TodoItem extends Component {
    static template = "awesome_owl.todo_item";
    static components = { Card };

    static props = { todo: { type: Todo }, onRemove: { type: Function } };

    toggle() {
        this.props.todo.isCompleted = !this.props.todo.isCompleted;
    }

    remove() {
        this.props.onRemove(this.props.todo.id);
    }
}

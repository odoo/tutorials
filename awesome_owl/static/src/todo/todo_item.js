import { Component, useState } from "@odoo/owl";
import { useAutoFocus } from "../utils/utils";

export class TodoItem extends Component {
    static props = ["todo", "toggleState", "removeTodo"];
    static template = "awesome_owl.todo_item";

    change() {
        this.props.toggleState(this.props.todo.id);
    }

    remove() {
        this.props.removeTodo(this.props.todo.id);
    }
}
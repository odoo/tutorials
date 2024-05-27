/** @odoo-module **/

import { Component } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.todo_item";
    static props = {
        todo: {type: Object, shape: {id: Number, description: String, isCompleted: Boolean}},
        setCompleted: {type: Function},
        deleteTask: {type: Function},
    };

    onCheckboxChangeUpdateCompleted(event) {
        this.props.setCompleted?.(this.props.todo.id, event.target.checked);
    }

    onClickDeleteItem() {
        this.props.deleteTask?.(this.props.todo.id);
    }
}

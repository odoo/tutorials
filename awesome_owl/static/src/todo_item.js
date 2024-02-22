/** @odoo-module **/

import { Component } from "@odoo/owl";

export class TodoItem extends Component {

    static template = "awesome_owl.todo_item"

    static props = {
        item : {
            type:Object, 
            shape: {
                id: Number,
                description: String,
                isCompleted: Boolean
            }
        },
        toggleState: Function,
        removeTodo: Function
    }

    toggleCheckbox(ev) {
        this.props.toggleState(this.props.item.id, ev.target.checked);
    }

    deleteItem() {
        this.props.removeTodo(this.props.item.id);
    }
}

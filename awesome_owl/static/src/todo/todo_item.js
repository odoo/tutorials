/** @odoo-module **/

import { Component } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.todo_item";

    static props = {
        todo : {
            id: Number,
            description: String,
            isCompleted: Boolean
        },
        toggleState : Function
    }

    onChange(){
        this.props.toggleState(this.props.todo.id)
    }
}

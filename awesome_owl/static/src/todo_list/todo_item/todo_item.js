/** @odoo-module **/

import { Component, useState, markup} from "@odoo/owl";


export class TodoItem extends Component {
    static template = "awesome_owl.todo_item";

    static props = {
        todo: {type: Object, shape: {id: Number, description: String, isCompleted: Boolean}},
        index: Number,
        checkboxAction: Function,
        removeAction: Function
    }

    checkboxChanged() {
        this.props.checkboxAction(this.props.index)
    }

    removed() {
        this.props.removeAction(this.props.index)
    }
}

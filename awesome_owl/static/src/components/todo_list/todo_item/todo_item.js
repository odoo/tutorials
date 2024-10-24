/** @odoo-module **/

import {Component} from "@odoo/owl";

export class TodoItem extends Component {

    static props = {
        todo: {
            type: Object
        },
        list: {
            type: Object
        },
    }

    static template = "awesome_owl.todo_item";

    toggle() {
        this.props.list.toggleItem(this.props.todo.id)
    }

    delete() {
        this.props.list.deleteItem(this.props.todo.id)
    }
}

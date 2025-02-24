/** @odoo-module **/

import { Component } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.todo_item";

    static props = {
        id: {
            type: Number
        },
        description: {
            type: String
        },
        isCompleted: {
            type: Boolean
        },
        toggleState: {
            type: Function,
            optional: true
        }
    }

    onStateChange() {
        if (this.props.toggleState) {
            this.props.toggleState(this.props.id);
        }
    }
}

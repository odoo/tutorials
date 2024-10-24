/** @odoo-module **/

import { Component } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.todo_item";

    static props = {
        id: { type: Number },
        description: { type: String },
        isCompleted: { type: Boolean },
        callback: { type: Function },
        delCallback: { type: Function },
    };

    setup() {
        this.toggleCompletion = this.toggleCompletion.bind(this);
        this.callDelete = this.callDelete.bind(this);
    }

    toggleCompletion() {
        this.props.callback(this.props.id);
    }

    callDelete() {
        this.props.delCallback(this.props.id);
    }
}

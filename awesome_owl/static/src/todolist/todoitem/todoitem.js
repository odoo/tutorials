import { Component, useState } from "@odoo/owl";

export class TodoItem extends Component {
    static template = 'awesome_owl.todoitem';

    static props = {
        id: { type: Number },
        description: { type: String },
        isCompleted: { type: Boolean },
        toggleState: { type: Function },
        removeTodo: { type: Function },
    };

    setup() {
        this.callToggleState = this.callToggleState.bind(this);
        this.callRemoveTodo = this.callRemoveTodo.bind(this);
    }

    callToggleState() {
        this.props.toggleState(this.props.id);
    }

    callRemoveTodo() {
        this.props.removeTodo(this.props.id);
    }
}

import { Component, useState } from '@odoo/owl'


export class TodoItems extends Component {
    static template = 'todoitems';
    static props = {
        todo: { type: Object, shape: { id: Number, description: String, isCompleted: Boolean } },
        toggleState: { type: Function },
        removeState: {type: Function}
    }

    onChange() {
        this.props.toggleState(this.props.todo.id)
    }

    onRemove() {
        this.props.removeState(this.props.todo.id)
    }
}

/** @odoo-module **/

import { Component } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.todo_item"; 
    static props = {
        todo: {
            type: Object,
            shape: {
                id: Number,
                description: String,
                isCompleted: Boolean,
            },
        },
        toggleState: {type: Function, optional: true},
        removeTodo: {type: Function, optional: true},
    };

    toggled(){
        const id = this.props.todo.id
        this.props.toggleState?.(id);
    }

    removed(){
        const id = this.props.todo.id
        this.props.removeTodo?.(id)
    }
}

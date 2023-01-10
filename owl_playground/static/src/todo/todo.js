/** @odoo-module **/

import { Component } from "@odoo/owl";

export class Todo extends Component {
    onClick(ev) {
        this.props.toggleState(this.props.id); //We call the toggleState method of the parent component when the user clicks on the todo
    }

    onRemove(ev) {
        this.props.removeTodo(this.props.id)
    }
}

Todo.template = "owl_playground.todo";
Todo.props = {
    id: { type: Number },
    description: { type: String },
    done: { type: Boolean },
    toggleState: { type: Function }, //We add the toggleState method as a prop
    removeTodo: { type: Function },
};
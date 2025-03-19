/** @odoo-module **/

import { Component } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.TodoItem";

    toggleState(){
        this.props.onToggle(this.props.todo);
    }

    removeTodo(){
        this.props.onRemove(this.props.todo);
    }
}

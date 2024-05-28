/** @odoo-module **/

import { Component } from "@odoo/owl";


export class TodoItem extends Component {
    static template = "awesome_owl.todo_item";
    static props = {
        todo: {
            id: Number,
            description: String,
            isCompleted: Boolean,
        },
        toggleState: Function,
        removeTodo: Function,
    };

    onChecked(){
        this.props.toggleState(this.props.todo.id);
        // console.log(this.props.todo.id);
    }

    onRemoveTodo(){
        this.props.removeTodo(this.props.todo.id);
    }
}
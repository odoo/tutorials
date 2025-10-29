/** @odoo-module alias=@awesome_owl/todo_list/TodoItem default=false**/

import { Component } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.TodoItem";
    static props = {
        todo: {
            type: Object,
            shape: { id: Number, description: String, isCompleted: Boolean }
        },
        toggleState: Function,
        deleteState: Function,
    };

    onChange() {
        this.props.toggleState(this.props.todo.id);
    }
    
    onDelete(){
        this.props.deleteState(this.props.todo.id)
    }
}

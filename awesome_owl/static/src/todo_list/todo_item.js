/** @odoo-module **/

import { Component } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.TodoItem";

    static props = {
        todo: {
            type: Object,
            shape: {
                id: Number,
                description: String,
                isCompleted: Boolean,
            },
        },
        toggleTodoState: Function,
    }

    checkboxStateChanged(){
        if(this.props.toggleTodoState){
            this.props.toggleTodoState(this.props.todo.id)
        }
    }

}

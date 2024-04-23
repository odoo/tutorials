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
        toggleTodoItemState: Function,
        removeTodoItem: Function,
    }

    toggleTodoItemState(){
        this.props.toggleTodoItemState(this.props.todo.id)
    }

    removeTodoItem(){
        this.props.removeTodoItem(this.props.todo.id)
    }
    

}

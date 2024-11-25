/** @odoo-module **/

import { Component } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.todoitem";
    static props = { 
        todo : {type: Object, shape: {id : Number, description: String, isCompleted: Boolean }},
        todoListToggleItem : { type : Function, optional : false },
        todoListRemoveItem : { type : Function, optional : false }
    }
    todoItemToggleItem() {
        this.props.todoListToggleItem(this.props.todo.id);
    }
    todoItemRemoveItem() {
        this.props.todoListRemoveItem(this.props.todo.id);
    }
}

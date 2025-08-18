/** @odoo-module **/

import { Component, useState} from "@odoo/owl";

export class TodoItem extends Component {
    
    static template = "awesome_owl.todoitem";
    static props = {
        id: { type: Number},
        description: { type: String},
        isCompleted: { type: Boolean},
        toggleState: { type: Function},
        removeTodo: { type: Function}
    }

    checkBoxChange(e){
        const check = e.target.checked;
        this.props.toggleState(this.props.id, check);
    }

    deleteTodo(){
        this.props.removeTodo(this.props.id)
    }

}

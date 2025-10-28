/** @odoo-module **/

import { Component } from "@odoo/owl"

export class ToDoItem extends Component{
    static template = "awesome_owl.to_do_item"
    static props = {
        todo : {
            type: Object, 
            shape : {id: Number, description: String, isComplete: Boolean}
        },
        toggleState: {
            type: Function,
            optional: true
        }
    }
    
    setState(todo) {
        this.props.toggleState(todo);
    }
    
}

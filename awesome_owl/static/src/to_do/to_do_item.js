/** @odoo-module **/

import { Component } from "@odoo/owl"

export class ToDoItem extends Component{
    static template = "awesome_owl.to_do_item"
    static props = {
        todo : {
            type: Object, 
            shape : {id: Number, description: String, isComplete: Boolean}
        },
        deleteToDo: {
            type: Function,
            optional: true,
        }
    }

    setup(){
        this.toggleState = this.toggleState.bind(this);
    }
    
    toggleState() {
        this.props.todo.isComplete = !this.props.todo.isComplete
    }

    removeToDo() {
        if(this.props.todo){
            this.props.deleteToDo(this.props.todo.id)
        }
    }
    
}

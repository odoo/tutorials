import { Component, useRef, onMounted, useState } from "@odoo/owl";


export class TodoItem extends Component {
    static template = "awesome_owl.todo_item";
    static props = {
        id: {type: Number},
        description: {type: String},
        isCompleted: {type: Boolean},
        onClick : { Type: Function, optional : true },
    }
    
    toggleState(){
        this.props.isCompleted = !this.props.isCompleted;
    }

    removeTodo() {
        this.props.onClick(this.props.id);
    }
}

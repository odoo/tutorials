import { Component, useState } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.todo_item";
    static props = {
        todo: { 
            type: Object,
            shape: { 
                id: {type: Number, optional: false},
                description: {type: String, optional: false}, 
                isCompleted: {type: Boolean, optional: false}, 
            },
        },
        toggleState: {
            type: Function,
            optional: false,
        },
        removeTodo: {
            type: Function,
            optional: false,
        },
    };

    change(){
        this.props.toggleState(this.props.todo.id);
    }
    remove(){
        this.props.removeTodo(this.props.todo.id);
    }

}

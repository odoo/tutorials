import { Component, useState } from "@odoo/owl";

export class TodoItem extends Component 
{
    static template = 'awesome_owl.TodoItem';
    static props = {
        todo : {
            type: Object, 
            shape:{
                id: {type : Number},
                description: {type : String},
                isCompleted: {type: Boolean}}
            },

        updateState : {
            type: Function,
        },

        deleteTodo : {
            type : Function,
            optional: true
        }
    };
    
    updateState(event)
    {
        this.props.updateState(this.props.todo.id);
    }
    deleteTodo(event)
    {
        this.props.deleteTodo(this.props.todo.id);
    }
}
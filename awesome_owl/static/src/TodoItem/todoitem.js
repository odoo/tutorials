import { Component } from "@odoo/owl";


export class TodoItem extends Component {
    static template = "awesome_owl/TodoItem";
    static props = {
        todo:{
            type: Object, 
            optional: false
        },
        toggleStart: Function,
        deleteTodo: Function
    };

    toggleCompleted() {
        this.props.toggleStart(this.props.todo);
    }
    
    removeTodo() {
        this.props.deleteTodo(this.props.todo.id);
    }
}

import { Component } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.todo_item";
    static props = {
        todo: { type: Object, required: true },
        toggleState: { type: Function, required: true },
        removeTodo: { type: Function, required: true },
    };

    toggleState = () => {
        this.props.todo.isCompleted = !this.props.todo.isCompleted;   
    }

    removeTodo = () =>{
        this.props.removeTodo(this.props.todo.id);
    }
    
}
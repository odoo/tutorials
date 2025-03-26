import { Component, List } from "@odoo/owl";

export class TodoItem extends Component{
    static template = "awesome_owl.todoitem";
   

    static props = {
        todo: {
            type: Object,
            shape: {
                id: { type: Number, required: true },
                description: { type: String, required: true },
                isCompleted: { type: Boolean, required: true },
            }
        },
        toggleState: { type: Function, required: true },
        removeTodo: { type: Function, required: true },
    };
    toggleCompletion(){
        this.props.toggleState(this.props.todo.id);
    };
    remove(){
        this.props.removeTodo(this.props.todo.id);
    };
}
import {Component} from "@odoo/owl";

export class TodoItem extends Component{
    static template="awesome_owl.todoItem"
    static props={
        todo: { type: Object, shape: { id: Number, description: String, isCompleted: Boolean } },
        toggleState:Function,
        removeTodo:Function
    }
    toggle(){
        this.props.toggleState(this.props.todo.id)
    }
    remove(){
        this.props.removeTodo(this.props.todo.id)
    }
}

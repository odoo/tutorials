import { Component } from "@odoo/owl";


export class TodoItem extends Component {
    static template = "awesome_owl.todoitem";
    static props = {
        todo: Object,
        toggleState: Function,
        removeTodo: Function
    };

    toggleIsCompleted(){
        this.props.toggleState(this.props.todo.id)
    }

    onClickRemove(){
        this.props.removeTodo(this.props.todo.id)
    }
}

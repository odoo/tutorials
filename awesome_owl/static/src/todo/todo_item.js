import { Component } from "@odoo/owl"

export class TodoItem extends Component {
    static template = "awesome_owl.TodoItem"

    static props = {
        todo:{
            id:Number,
            description:String,
            isCompleted:Boolean,
        },
        toggleState: Function,
        removeTodo: Function,
    }

    onToggle(){
        this.props.toggleState(this.props.todo.id)
    }

    onRemove(){
        this.props.removeTodo(this.props.todo.id)
    }
}

import { Component } from '@odoo/owl'


export class TodoItem extends Component {
    static template = "awesome_owl/TodoItem"
    static prop = {
        type: Object,
        shape : {
            id : {
                type: Number
            },
            description: {
                type: String
            },
            isCompleted: {
                type: Boolean
            }
        },
        toggleStart: Function,
        deleteTodo: Function

    }

    toggleCompleted() {
        this.props.toggleStart(this.props.todo)
    }
    
    removeTodo() {
        this.props.deleteTodo(this.props.todo)
    }
}

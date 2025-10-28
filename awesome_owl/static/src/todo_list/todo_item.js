import { Component } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.TodoItem";

    static props = {
        item : {
            type: Object,
            shape: {
                id: Number,
                description: String,
                isCompleted: Boolean,
            }
        },
        toggleState : {
            type: Function,
            optional: true,
        },
        deleteTodo : {
            type: Function,
            optional: true,
        }
    }

    onChangeCheck (id){
        // this.props.toggleState(id)
        this.props.item.isCompleted = !this.props.item.isCompleted
    }

    onClickDelete (id){
        this.props.deleteTodo(id)
    }
}

import { Component } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.TodoItem";

    static props = {
        todo: {
            type: Object,
            shape: {
                id: Number ,
                description:  String ,
                isCompleted: Boolean 
            }
        },
        toggleState: {type: Function},
        removeItem: {type: Function}
    };

    onChange(){
        this.props.toggleState(this.props.todo.id)
    }

    onClickRemoveItem(){
        this.props.removeItem(this.props.todo.id)
    }


}
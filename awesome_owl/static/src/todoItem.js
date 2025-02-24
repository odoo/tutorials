import {Component} from "@odoo/owl";

export class TodoItem extends Component{

    static template = "awesome_owl.TodoItem";

    static props= {
        todo : {
            type : Object,
            shape : {
                id : Number,
                description : String,
                isCompleted : Boolean
            }
        },
        changed_checkbox : Function ,
        removeTodo : Function
    };

    changed_checkbox(){
        this.props.changed_checkbox(this.props.todo.id);
    }

    removeTodo(){
        this.props.removeTodo(this.props.todo.id);
    }

}
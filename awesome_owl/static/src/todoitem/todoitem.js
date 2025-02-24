import { Component } from "@odoo/owl"

export class ToDoItem extends Component{
    static template = "awesome_owl.todoitem"
    static props= {
        id:{type: Number},
        description:{type: String},
        isCompleted:{type: Boolean},
        onToggleStatus:{type: Function, optional: true},
        onDelete:{type: Function, optional: true},
    };
    toggleStatus(){
        this.props.onToggleStatus(this.props.id);
    }
    onDelete(){
        this.props.onDelete(this.props.id);
    }
}

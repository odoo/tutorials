import {Component} from '@odoo/owl'

export class TodoItem extends Component{
    static template = "awesome_owl.todoItem";
    static props = {
        todo:{
            type: Object,
            shape:{
                id:Number,
                description:String,
                isCompleted:Boolean,
            }
        },
        onChange:{
            type:Function,
        },
        onDelete:{
            type:Function
        }
    }   

    markComplete(){        
        this.props.onChange(this.props.todo.id)
    }

    deleteTodo(){
        console.log("Todo Item",this.props.todo);
        this.props.onDelete(this.props.todo.id)
        
    }

}
import { Component } from "@odoo/owl";
export class TodoItem extends Component {
    static template = "awesome_owl.todo_item";
    static props = {
        todo: {
            type: Object,
            shape: {
                id: Number,
                description: String,
                isCompleted: Boolean,
            },
            optional: false,
        },
        toggleState: Function,
        removeTodoItem:Function
    }
    onCheckboxChange=()=> {
        console.log("Checked click ! ! ! ")
        this.props.toggleState(this.props.todo.id);
    }
    removeTodo=()=>{
        console.log("Clicked remove ")
        
        this.props.removeTodoItem(this.props.todo.id);
    }
}
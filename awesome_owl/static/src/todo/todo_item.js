import {Component} from "@odoo/owl"

export class TodoItem extends Component{
    static template = "awesome_owl.todo_item"
    static props = {
        todo: {type: {id: Number, description: String, isCompleted: Boolean}},
        toggleCompleted: {type: Function, optional:true},
        deleteTodo: {type: Function, optional:true},
    }

}
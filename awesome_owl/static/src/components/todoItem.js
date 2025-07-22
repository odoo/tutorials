import { Component } from "@odoo/owl";

export class TodoItem extends Component{

    static template = "awesome_owl.todoItem";
     static props = {
         todo: Object,
         callback: {type : Function, optional: true},
         deleteTodo:{type : Function, optional: true}
     }

     onClickCheckbox()
     {
        this.props.callback(this.props.todo.id);
     }
}

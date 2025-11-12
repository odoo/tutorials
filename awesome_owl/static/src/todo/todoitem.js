import { Component } from "@odoo/owl";

export class TodoItem extends Component{

    static template = "awesome_owl.todoitem";

    static props ={
        todo : {
            id : {type: Number},
            description : {type: String},
            isCompleted : {type: Boolean},
        },
        toggleState : {
            type: Function,
            optional : false,
        },

        removeTodo : {
            type: Function,
            optional : false,
        }
    };

}

import { Component } from "@odoo/owl"

export class TodoItem extends Component{
    static template = "awesome_owl.todoitem"

    static props = {
        // index : {type : Integer},
        todo: {type: Object},
        callback : {type : Function},
        removecallback : {type : Function}
    }
}

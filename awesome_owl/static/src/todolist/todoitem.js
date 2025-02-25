import { Component } from "@odoo/owl";

export class ToDoItem extends Component {
    static template = "awesome_owl.ToDoItem";
    static props = {
        todo : {type: Object, shape: {id: Number, description: String, isCompleted: Boolean}},
        toggleState : Function,
        removeTodo: Function,
    }
}
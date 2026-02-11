/** @odoo-module **/
import { Component } from "@odoo/owl";

export class TodoItem extends Component {

    static template = "awesome_owl.TodoItem";
    static props = {
        todo: { type: Object, 
                required: true },
        toggleState: { type: Function, 
                        required: true },
        removeTodo: { type: Function, 
                        required: true },
    };
}
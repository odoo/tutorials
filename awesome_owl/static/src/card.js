/** @odoo-module **/

import { Component } from "@odoo/owl";
import { Counter } from "./counter";
import { TodoList } from "./todo_list";

export class Card extends Component {
    static template = "awesome_owl.card"; 
    static components = { Counter, TodoList };
    static props = {
        slots: {
            type: Object,
        },
        title: {type: String},
        active: {type: Boolean, default: true},
        onChange: {type: Function, optional: true},
        id: {type: Number}
    }
        

    minimize(){
        this.props.onChange?.(this.props.id)
    }
}

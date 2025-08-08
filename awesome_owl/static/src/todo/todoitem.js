/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.todoitem";
    static props ={
        todo : {
            type : Object,
            optional : false
        },
        toggleState : {type : Function, optional : false},
        removeTodo : {type : Function, optional : false}
    };
}

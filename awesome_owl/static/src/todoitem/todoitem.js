/** @odoo-module **/

import { Component, useState } from "@odoo/owl";


export class TodoItem extends Component{
    static template = "awesome_owl.Todoitem";
    static props = {
        todo: {
            type:Object,
            shape: {id: Number, description: String, isComplete: Boolean}
        }
    }
}

import { Component , useState } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.todo_item";

    static components = { }

    static props = ['todo','toggleState','removeItem']

    setup(){
    }
}
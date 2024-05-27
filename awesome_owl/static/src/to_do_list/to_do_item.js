/** @odoo-module **/

import {Component} from "@odoo/owl";

export class Item extends Component {
    static template = "awesome_owl.to_do_item";
    static props = {todo:{},toggleState:{},removeTodo:{}};
    check() {
        this.props.toggleState(this.props.todo.id);
    }
    rmTodo(){
        this.props.removeTodo(this.props.todo.id);
    }
}
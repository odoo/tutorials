/** @odoo-module **/
import {Component} from "@odoo/owl";
import {Todo} from "./todos";

export class TodoItem extends Component {
    static template = 'awesome_owl.TodoItem';
    static props = {
        todo: Todo,
    };
}

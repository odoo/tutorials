/** @odoo-module **/

import { Component,useState , markup } from "@odoo/owl";
import { Counter } from "./counter/Counter";
import { Card } from "./card/Card";
import { TodoList } from "./todo_list/todo_list";


export class Playground extends Component {
    static template = "awesome_owl.playground";

    static components = { Counter, Card , TodoList};
    setup(){
        this.str1 = "<div class='text-primary'> some content</div>"
        this.str2 = markup("<div class='text-danger'> some content</div>")
        this.sum = useState({value : 2})
    }

    incrementSum(){
        this.sum.value = this.sum.value + 1;
    }

}

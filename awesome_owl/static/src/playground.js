/** @odoo-module **/

import { Component, useState, markup} from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo_list/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = {Counter, Card, TodoList}
    setup(){
        this.safeHtml = markup("<div class='text-primary'>India</div>")
        this.sum = useState({value:2});
        this.incrementSum = this.incrementSum.bind(this);
    }
    incrementSum(x){
        this.sum.value += x
    }
}

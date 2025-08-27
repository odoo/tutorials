/** @odoo-module **/

import { Component , useState , markup} from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card"; 
import { TodoList } from "./todo/TodoList";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter,Card,TodoList };
    setup(){
        this.state=useState({sum:2})
        this.Title="My Title",
        this.safeContent="<div class='text-primary'>This is a string</div>",
        this.markupContent=markup("<div class='text-primary'>This is a string</div>")
    }
    incrementSum(){
        this.state.sum++;
    }
}

/** @odoo-module **/

import { Component ,markup, useState} from "@odoo/owl";
import { Counter } from "./counter/Counter";
import { Card } from "./card/Card";
import { TodoList } from "./todo/todo_list";


export class Playground extends Component {
    static template = "awesome_owl.playground";
    static props={}
   
    
    static components = {Counter, Card, TodoList};
    setup(){

        this.normalText = "This <em>will be escaped</em>";
        this.markupText = markup("This <em>will not be escaped</em>");

        this.state = useState({ sum: 0});
        this.incrementSum =this.incrementSum.bind(this)
    }

    incrementSum(){
        this.state.sum++;
    }
}

/** @odoo-module **/

import {markup, Component , useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { Todolist } from "./todo/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static props ={
        
    }
    value2 = markup("<div>some text 2</div>");
    static components = { Counter , Card , Todolist}; 

    state= useState({
        sum:0,
        card1:false,
        card2:false
    })
    incrementsum= ()=> {
        this.state.sum++;
    }
    inccard1= ()=> {
                this.state.card1= !this.state.card1;

    }
    inccard2= ()=> {
               this.state.card2= !this.state.card2;

    }
}

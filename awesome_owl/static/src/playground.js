/** @odoo-module **/

import { Component, markup, useState } from "@odoo/owl";
import { Card } from "./card";
import { Counter } from "./counter";
import { TodoList } from "./todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList };
    static props = [];

    value1 = "<div class='text-primary'>some content</div>";
    value2 = markup("<div class='text-primary'>some content</div>");

    setup() {
        this.state = useState({ 
            value: 2 ,            
            card1Active: true,
            card2Active: true,
            card3Active: true,
        });
    }

    incrementSum(){
        this.state.value++;
    }

    toggle(id){
        if (id ===1){
            this.state.card1Active = !this.state.card1Active
        }
        else if (id ===2){
            this.state.card2Active = !this.state.card2Active
        }
        else if (id ===3){
            this.state.card3Active = !this.state.card3Active
        }
    }
}

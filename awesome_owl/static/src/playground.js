import { Component, useState } from "@odoo/owl";
import Counter from "./counter/counter";
import Card from "./card/card";
import {TodoList} from "./todo/todoList";
import { markup } from "@odoo/owl";

export class Playground extends Component {
    static template = "awesome_owl.Playground";
    static components = { Counter, Card , TodoList};

    setup() {
        this.card1Content = markup("<strong>Bold text</strong>"); 
        this.state = useState({
            sum: 2
        });
    }
    
    incrementSum() {
            this.state.sum++;
    }
    
   
}

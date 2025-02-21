/** @odoo-module **/

import { Component , useState ,markup } from "@odoo/owl";
import { Counter } from "./counter";
import { Card } from "./card";
import { TodoList } from "./todoList"
export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter , Card , TodoList };
    setup(){
        this.state = useState({
            sum:2
        });
         // Binding incrementSum to ensure 'this' refers to Playground
        this.incrementSum = this.incrementSum.bind(this); 
        this.cardTitle = "My First Card";
        this.cardContent = "This is <strong>bold</strong> text!";
        this.safeContent = markup("This is <strong>bold</strong> text!");
        
    }

    incrementSum(){
        this.state.sum++;
    }

}



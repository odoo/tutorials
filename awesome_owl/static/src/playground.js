/** @odoo-module **/

import {Component , useState} from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./TodoList";

export class Playground extends Component{ 

        static template = "awesome_owl.Playground"; 
        static components = {Counter , Card , TodoList};

        setup() {
        
        this.sum = useState({value : 0});
        this.cards = [
            { title: "Card 1", content: "122" },
            { title: "Card 2", content: "This is the content for Card 2." },
            { title: "Card 3", content: "This is the content for Card 3." }
        ];

        this.incrementSum = () => {
              
            this.sum.value++;
        }
    }
}

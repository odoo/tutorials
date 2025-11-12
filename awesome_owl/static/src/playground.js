/** @odoo-module **/

import {Component , useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo_list/TodoList";

export class Playground extends Component{ 

        static template = "awesome_owl.Playground"; 
        static components = {Counter , Card , TodoList};

        setup() {
        
        
        this.sum = useState({value : 0});
       

        this.incrementSum = () => {
              
            this.sum.value++;
        }
    }
}

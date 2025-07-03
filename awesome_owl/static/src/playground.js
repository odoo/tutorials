/** @odoo-module **/

import { Component , useState } from "@odoo/owl";
import { Counter } from "./counter";
import { TodoList } from "./todo/todo_list";
import { Card } from "./card";

export class Playground extends Component {
    static template = "awesome_owl.playground";

    static components = { Counter ,TodoList , Card}

    setup(){
        this.sum = useState({value:0})
    }

    increment(){
        this.sum.value++;
    }
}

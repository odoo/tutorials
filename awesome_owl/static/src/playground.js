/** @odoo-module **/

import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo/todolist";

export class Playground extends Component {
    static template = "awesome_owl.playground";

    setup(){
        this.content1 = '<div class="text-primary" >some content</div>';
        this.content2 = markup('<div class="text-primar" >some content</div>');
        this.sum = useState({value:2})
    }

    incrementSum(sum){
        this.sum.value++;
    }
    static components = { Counter, Card, TodoList };

}

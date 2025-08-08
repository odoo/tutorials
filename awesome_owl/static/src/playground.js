/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { ToDoList } from "./todolist/todolist";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, ToDoList }
    // title = markup("<div>I am a title</div>")
    // content = markup("<div>some content</div>")
    
    setup() {
        this.sum = useState({value: 2 });
        
    }

    incrementSum() {
        this.sum.value++;
    }

}

import { Component, markup, useState } from "@odoo/owl";
// import { Todolist } from "./components/todolist/todolist.js";
import { Card } from "./components/card/card.js";
import { Counter } from "./components/counter/counter.js";


export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Card, Counter };
    

    setup() {
    }

}

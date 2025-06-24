/** @odoo-module **/
import { Card } from "./card/card";
import { Counter } from "./counter/counter";
import { TodoList } from "./todolist/todolist";
import { Component, useState, markup} from "@odoo/owl";

export class Playground extends Component {
    static template = "awesome_owl.playground";

    static components = {Counter,Card,TodoList}

    setup() {
        this.state = useState({ safe_title: markup("<div class='text-primary'>some content</div>"), sum:0 });
    }

    incrementSum(){
        this.state.sum++;
    }

}


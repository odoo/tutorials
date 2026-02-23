import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter";
import { Card } from "./card"
import { TodoList } from "./todo_list";


export class Playground extends Component {
    static template = "awesome_owl.playground";
    static props = []
    static components = {Counter, Card, TodoList}

    html1 = "<div class='text-primary'>some content</div>";
    html2 = markup("<div class='text-primary'>some content</div>");

    setup(){
        this.state = useState({sum: 2});
    }

    incrementSum(){
        this.state.sum +=1;
        console.log('Incrementing sum by 1 ->', this.state.sum)
    }
}

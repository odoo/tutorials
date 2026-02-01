import { Component, markup, useState} from "@odoo/owl";
import {Card} from "./card/card";
import {Counter} from "./counter/counter";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = {Card, Counter};

    setup(){
        this.state = useState({sum: 2});
        this.cardContent = markup("<b>Card 1</b> content of card1");
    }
    incrementSum(){
        this.state.sum++;
    }
}

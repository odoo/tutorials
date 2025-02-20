/** @odoo-module **/

import { Component, markup } from "@odoo/owl";
import { Counter } from "./counter";
import { Card } from "./card";
import { Sum } from "./sum";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, Sum};

    setup(){
        this.cards=[
        { title : "card1", content: "This is normal text"},
        {title : "card2", content: markup("<strong>This is bold text</strong>")},
        {title : "card3", content: "<strong>This is bold text</strong>"},
    ];
    }
}

import { Component, useState, markup } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { GlobalCounter } from "./global_counter/global_counter";

export class Playground extends Component {
    setup(){
        this.normal_string = "normal string"
        this.html_string = markup("<a href=https://www.w3schools.com>Visit W3Schools.com!</a>")
    }

    static template = "awesome_owl.playground";
    static components = { 
        Counter,
        Card,
        GlobalCounter
    }
}

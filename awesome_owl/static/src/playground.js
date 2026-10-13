import { Component, useState, markup } from "@odoo/owl";
import { Counter } from "./counter";
import { Card } from "./card";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card };

    setup(){
        this.html = markup("<div class='text-primary'>This html is rendered in blue.</div>");
        this.plainText = "<div class='text-primary'>This is plain text,not HTML.</div>";
    }
}

/** @odoo-module **/

import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter";
import { Card } from "./card";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components= {Counter, Card};

    setup(){
        this.safehtml= markup("<strong>This is bold HTML content</strong>");
        this.escapedText= "<strong>This is bold HTML content</strong>";
        this.sum= useState({value:0})
    }
    incrementSum(){
        this.sum.value++;
    }
}

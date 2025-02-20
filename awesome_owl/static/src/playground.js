/** @odoo-module **/

import { Component , useState ,markup } from "@odoo/owl";
import { Counter } from "./counter";
import { Card } from "./card";
export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter , Card};
    setup(){
        this.cardTitle = "My First Card";
        this.cardContent = "This is <strong>bold</strong> text!";
        this.safeContent = markup("This is <strong>bold</strong> text!");
    }

}



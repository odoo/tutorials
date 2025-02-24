/** @odoo-module **/
import { Component, markup, useState } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.Card";
    static props = {
        title: { type: String, optional: false },
        content: { type: String, optional: true },
    };
    setup(){
        this.isOpen = useState({ value: true }); 
    }

    toggleCard() {
        this.isOpen.value = !this.isOpen.value; 
    }
    
    value1 = markup("<div>some text 1</div>");
    value2 = markup("<div>some <br> text 2</div>");
}

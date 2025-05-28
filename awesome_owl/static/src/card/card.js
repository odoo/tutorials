/** @odoo-module **/

import { Component, useState} from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.card";
    static props = {
        title: String,
        slots: Object,
        // content: String
    };
    
    setup() {
        this.isOpen = useState({value:true});
    }

    toggleCardVisibility() {
        this.isOpen.value = !this.isOpen.value;
    }

}

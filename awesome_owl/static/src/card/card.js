/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.card";
    static props = {
        title: {type: String},
        slots: {type: Object}
    };

    setup (){
        this.state = useState({ value:0, open:true});
    }

    onChange (){}

    toggleVisible(){
        this.state.open = !this.state.open;
    }

}

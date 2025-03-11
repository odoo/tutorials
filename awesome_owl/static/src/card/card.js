/** @odoo-module **/

import { Component, useState } from "@odoo/owl";


export class Card extends Component{
    static template = "awesome_owl.Card";
    static props = {
        title : String,
        slots : { type: Object, optional: true},
    };
    setup(){
        this.state = useState({value : true})
    }
    toggleContent(){
        this.state.value = !this.state.value
    }
}

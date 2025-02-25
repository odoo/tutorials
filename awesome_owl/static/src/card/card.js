/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.Card";
    static props = {
        title : String,
        slots : {Object, optional: true},
    };

    setup(){
        this.state = useState({value : true});
    }

    toggleText(){
        console.log("Hdguagdjw");
        this.state.value = !this.state.value;
    }
}

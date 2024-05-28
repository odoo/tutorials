/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.card";
    static props = {
        num: Number,
        slots:{},
    };
    setup(){
        this.hide=useState({value:false});
    }
    hideCard() {
        this.hide.value=!this.hide.value;
    }
}
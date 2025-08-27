import { Component, useState } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.card_template";
    static props = {
        title: { type: String, optional: true },
        content: { type: String, optional: true },
        slots: { type: Object, optional: true }
    };
    setup(){
        this.state=useState({isOpen:true})
    }
    togglecard(){
        this.state.isOpen=!this.state.isOpen;
    }
}

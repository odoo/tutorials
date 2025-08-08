import { Component, useState } from "@odoo/owl";
export class Card extends Component {
    static template = "awesome_owl.card";
    static props= {
        'title':String,
        'content':String,
        'slots': { type:Object, optional:true}
    };
    setup(){
        this.state= useState({isOpen:true});
    }
    toggleContent(){
        this.state.isOpen= !this.state.isOpen;
    }
}

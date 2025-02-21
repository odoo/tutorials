import { Component, useState } from "@odoo/owl";
import { Counter } from "../counter/counter";

export  class Card extends Component{

    static template = "awesome_owl.Card";
    static components= {Counter}; 
    // props validation
    static props={
        title: String,
    };
    setup() {
        this.state = useState({ isOpen: true });
    }

    toggleContent() {
        this.state.isOpen = !this.state.isOpen;
    }
    
}

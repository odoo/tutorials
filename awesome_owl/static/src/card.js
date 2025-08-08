import { Component, useState } from "@odoo/owl";


export class Card extends Component {
    static template = "awesome_owl.card";
    
    static props = {
        title: {type: String},
        "*": true,
    }

    setup(){
        this.state = useState({visable: true});
    }

    toggleVisability() {
        this.state.visable = !this.state.visable
    }
}
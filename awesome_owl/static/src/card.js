import { Component, useState} from "@odoo/owl";

export class Card extends Component{
    static template = "estate.Card";

    static props = {title: {type: String, optional: false}, content: {type: String, optional: true},
     slots: {type:Object, optional: true} }

     setup() {
        this.state = useState({ isOpen: true }); 
    }

     toggleContent() {
        this.state.isOpen = !this.state.isOpen;
    }
}

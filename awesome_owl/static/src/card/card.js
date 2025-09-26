import { Component, useState } from "@odoo/owl";

export class Card extends Component {
   static template = "awesome_owl.Card"

    static props = {
        title: String,
        content:{
            type: String,
            optional: true,
        },
        slots: Object, // I added this to allow slots inside cards
    };

    setup(){
        this.state = useState({open : true});
    }

    onToggleVisibility() {
        this.state.open = !this.state.open;
    }
  
}


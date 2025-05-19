import { Component, useState } from "@odoo/owl";

export class Card extends Component{ 
    static template = "awesome_owl.cards";
    static props =  { 
        cardtitle:  {
            type: String,
            validate: e => e.includes("card"),
        },
        slots: {
            type: Object,
        },
    };

    setup(){ 
        this.state = useState({ opened: false });
    }

    toggleCounter(){
        this.state.opened = !this.state.opened;
    }
}

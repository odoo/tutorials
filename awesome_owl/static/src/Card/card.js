import { Component } from "@odoo/owl";

export class Card extends Component{ 
    static template = "awesome_owl.cards";
    static props =  { 
      cardtitle:  {
            type: String,
            validate: e => e.includes("card"),
        },
      cardtext: {type: String},
    };
}

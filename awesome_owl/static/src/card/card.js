import { Component } from "@odoo/owl";

export class Card extends Component{
    static template = "awesome_owl.card_template"
    static props = { 
        title: {type: String, optional:false},
        description: {type: String, optional:false} 
    }
}

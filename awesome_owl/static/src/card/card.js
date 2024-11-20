import { Component, useState } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.Card";
    static props = {
        title : String,
        body : String
    }
    setup() {
        
    }

  }

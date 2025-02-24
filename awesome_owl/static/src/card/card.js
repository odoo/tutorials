import { Component, useState} from "@odoo/owl";


export class Card extends Component{
    static template = "awesome_owl.card";

    static props = {
        title: String,
        content: String,
        slots: {
            type: Object,
        }
    };

}

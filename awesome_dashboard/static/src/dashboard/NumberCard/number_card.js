import { Component } from "@odoo/owl";

export class NumberCard extends Component{
    static template = "awesome_dashboard.numbercard_template";
    static props = {
        title : {type: String},
        value : {type: Number}
    }
}

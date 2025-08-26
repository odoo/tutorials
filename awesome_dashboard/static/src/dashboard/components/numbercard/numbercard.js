import { Component } from "@odoo/owl";

export class NumberCard extends Component{
    static template = "awesome_dashboard.numberCard";
    static props = {
        desc :  String,
        value :  Number
    }
}

import { Component, onWillStart, useState} from "@odoo/owl";
export class NumberCard extends Component {
    static template = "awesome_dashboard.NumberCard";
    static components = { };
    static props = {
        title: {type : String, optional: true},
        value: { type: Number, optional: true}
    };
}

import { Component } from "@odoo/owl";

export class InfoCard extends Component {
    static template = "awesome_dashboard.InfoCard"
    static props = {
        title: { type : String },
        value: { type: Number}
    }

}

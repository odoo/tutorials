import { Component } from "@odoo/owl";

export class StatCard extends Component {
    static template = "awesome_dashboard.StatCard";
    static props = {
        title: {type: String},
        value: {type: Number},
    }
}
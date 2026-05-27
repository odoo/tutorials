import { Component } from "@odoo/owl";
import { Piechart } from "../piechart/piechart";

export class PiechartCard extends Component {
    static template = "awesome_dashboard.piechart_card";
    static components = { Piechart: Piechart };
    static props = {
        title: {
            type: String,
        },
        values: {
            type: Object,
        },
    };
}

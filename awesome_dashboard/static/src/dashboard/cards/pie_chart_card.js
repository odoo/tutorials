import { Component, xml } from "@odoo/owl";
import { Card } from "./card"
import { PieChart } from "../pie_chart/pie_chart";

export class PieChartCard extends Component {
    static template = "awesome_dashboard.pie_chart_card";
    static components = { Card, PieChart };
    static props = {
        title: String,
        value: Object
    };
    static template = xml`
        <t t-esc="props.title"/>
        <PieChart data="props.value"/>
    `;
}

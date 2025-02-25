/** @odoo-module **/

import { Component, onWillStart, useRef, useEffect } from "@odoo/owl";
import { loadJS } from "@web/core/assets";


export class PieChart extends Component {
    static template = "awesome_owl.pie_chart";

    static props = { data: Object };

    setup() {
        this.canvasRef = useRef("canvas");
        onWillStart(() => loadJS("/web/static/lib/Chart/Chart.js"));
        useEffect(() => this.renderChart(), () => []);
    }

    renderChart(){
    console.log("render chart");
        if(this.chart){
            this.chart.destroy();
        }
        const ctx = this.canvasRef.el.getContext("2d");
        this.chart = new Chart(ctx, {
            type: "pie",
            data: this.props.data,
        });
        console.log(JSON.stringify(this.props.data));
    }
}

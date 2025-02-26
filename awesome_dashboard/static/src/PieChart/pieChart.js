import { Component, useEffect, useRef, onWillStart } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.pieChart";
    // static props = {
        
    // }

    setup(){
        this.canvasRef = useRef("canvas")
        onWillStart(() => loadJS("/web/static/lib/Chart/Chart.js"));
        useEffect(() => this.renderedChart());
    }

    renderedChart(){
        var ctx = this.canvasRef.el.getContext("2d");

        var data = {
            datasets: [{
                data: this.props.data,
                backgroundColor: ["#FF6384", "#36A2EB", "#FFCE56"]
            }],

            labels: this.props.labels,
        };
        var options = { responsive: true };

        new Chart(ctx, {
            type: 'pie',
            data: data,
            options: options
        });
    }
}

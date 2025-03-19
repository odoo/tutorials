import { Component, useEffect, useRef, onWillStart } from "@odoo/owl";
import { loadJS } from "@web/core/assets";
import { getColor } from "@web/core/colors/colors";


export class PieChart extends Component {
    static template = "awesome_dashboard.pieChart";

    setup(){
        this.canvasRef = useRef("canvas")
        onWillStart(() => loadJS("/web/static/lib/Chart/Chart.js"));
        useEffect(() => this.renderedChart());
    }

    renderedChart(){
        if(this.myChart) this.myChart.destroy();
        const color = this.props.keys.map((_, index) => getColor(index));
        var ctx = this.canvasRef.el.getContext("2d");

        var data = {
            datasets: [{
                data: this.props.values,
                backgroundColor: color
            }],

            labels: this.props.keys,
        };
        var options = { responsive: true };

        this.myChart = new Chart(ctx, {
            type: 'pie',
            data: data,
            options: options
        });
    }
}

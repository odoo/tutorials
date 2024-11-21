import { Component, onWillStart, useEffect, useRef } from "@odoo/owl";
import { loadJS } from '@web/core/assets';

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
    static props = {
        title : String,
        data : { type: Object }
    }
    setup(){
        this.chart = null;
        this.canvasRef = useRef("canvas");

        onWillStart(async() => {
            await loadJS("/web/static/lib/Chart/Chart.js");
        });

        useEffect(() => {
            this.renderChart(this.props.data);
            return () => {
                if (this.chart) {
                    this.chart.destroy();
                }
            };
        });
    }

    renderChart(data) {
        if (this.chart) {
            this.chart.destroy();
        }
        this.chart = new Chart(this.canvasRef.el, {
            type: 'pie',
            data: {
                labels: Object.keys(data),
                datasets: [{
                    label: '# of shirts',
                    data: Object.values(data),
                }]
            }
        });
    }
}

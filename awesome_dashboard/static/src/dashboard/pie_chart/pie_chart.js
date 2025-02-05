/** @odoo-module **/
import { Component, useRef, useEffect, onWillStart } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.pie_chart";
    static props = {
        data: { type: Object },
    };

    setup() {
        this.canvasRef = useRef('canvasRef');
        this.chart = null;

        onWillStart(async () => {
            await loadJS(["/web/static/lib/Chart/Chart.js"]);
        });


        useEffect(() => this.renderChart()) 
    }

    renderChart() {
        if (this.chart) {
            this.chart.destroy();
        }
        this.chart = new Chart(this.canvasRef.el, this.getChartConfig());
    }

    getChartConfig() {
        return {
            type: 'pie',
            data: {
                labels: Object.keys(this.props.data),
                datasets: [{
                    data: Object.values(this.props.data),
                    backgroundColor: [
                        '#f6c23e',
                        '#4169E1',
                        '#32a133', ,
                    ],
                }],
            },
        }
    }
}

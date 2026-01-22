import { Component, onWillStart, onWillUnmount, useEffect, useRef } from "@odoo/owl";
import { loadJS } from "@web/core/assets";


export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";

    static props = {
        chart_data: {type: Object},
    };

    setup() {
        this.canvasRef = useRef("pie_chart_canvas");
        this.chart = null;
        
        onWillStart(() => loadJS(["/web/static/lib/Chart/Chart.js"]));

        useEffect(() => this.renderChart());
        onWillUnmount(() => this.destroyChart());
    }

    renderChart() {
        this.destroyChart();
        this.chart = new Chart(
            this.canvasRef.el, 
            {
                type: "pie", 
                data: {
                    labels: Object.keys(this.props.chart_data),
                    datasets: [
                        {
                            label: "orders_by_size",
                            data: Object.values(this.props.chart_data),
                        },
                    ],
                },
            },
        );
    }

    destroyChart() {
        if (this.chart) {
            this.chart.destroy();
        }
    }
}

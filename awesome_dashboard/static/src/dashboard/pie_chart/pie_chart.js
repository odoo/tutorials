import { Component, onWillStart, useRef, onMounted } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.piechart";
    static props = {
        chart_data: { type: Object },
    };
    setup () {
        this.canvasRef = useRef("dashboard");
        onWillStart(() => loadJS(["/web/static/lib/Chart/Chart.js"]));
        onMounted(() => {
            this.renderChart();
        });
    }

    renderChart () {
        if (this.chart) {
            this.chart.destroy();
        }
        let labels = [];
        let keys = [];
        for (let size in this.props.chart_data) {
            labels.push(size);
            keys.push(this.props.chart_data[size]);
        }
        console.log("Labels:" + labels);
        console.log("Keys: " + keys);
        const config = {
            type: "pie",
            data: {
                labels: labels,
                datasets: [
                    {
                        data: keys,
                        label: "Size Distribution",
                    },
                ],
            },
            options: {
                responsive: true,
            },
        }
        this.chart = new Chart(this.canvasRef.el, config);
    }
}

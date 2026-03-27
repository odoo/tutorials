import { Component, onWillStart, onMounted, useRef, useEffect } from "@odoo/owl";
import { loadJS } from "@web/core/assets";


export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
    static props = {
        data: {type: Object}
    };

    setup() {
        this.canvasRef = useRef("canvas");
        this.chart = null;

        onWillStart(() => loadJS(["/web/static/lib/Chart/Chart.js"]));

        onMounted(() => {
            this.renderChart();
        });

        useEffect(() => {
            if (this.chart) {
                this.chart.data.labels = Object.keys(this.props.data);
                this.chart.data.datasets[0].data = Object.values(this.props.data);
                this.chart.update();
            }
        }, 
        () => [this.props.data]); 
    }

    renderChart() {
        const config = {
            type: 'pie',
            data: {
                labels: Object.keys(this.props.data),
                datasets: [{
                    data: Object.values(this.props.data),
                }]
            }
        };
        this.chart = new Chart(this.canvasRef.el, config);
    }
}


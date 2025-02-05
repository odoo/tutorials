import { Component, useRef, onWillStart, onMounted, useEffect } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.piechart";
    static props = {
        data: { type: Object },
    };

    setup() {
        this.canvasRef = useRef('canvasRef');
        this.chart = null;

        onWillStart(async () => {
            await loadJS(["/web/static/lib/Chart/Chart.js"]);
        });

        // onMounted(() => {
        //     this.renderChart();
        // });

        useEffect(()=> this.renderChart())
    }

    renderChart() {
        if (this.chart) {
            this.chart.destroy();}
        this.chart = new Chart(this.canvasRef.el, this.getChartConfig());
      }
  
    getChartConfig() {
        return {
            type: 'pie',
            data: {
                labels: this.props.labels,
                datasets: [{
                    data: Object.values(this.props.data),
                    backgroundColor: [
                        '#4e73df',
                        '#1cc88a',
                        '#36b9cc',
                    ],
                }],
            },
        }
    }
}

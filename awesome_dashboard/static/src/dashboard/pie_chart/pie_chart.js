import { loadJS } from "@web/core/assets";
import { Component, useRef, onWillStart, onMounted, onWillUpdateProps, onWillUnmount } from "@odoo/owl";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
    static props = {
        label: String,
        data: Object,
    };

    setup() {
        this.canvasRef = useRef("canvas");
        onWillStart(() => loadJS("/web/static/lib/Chart/Chart.js"));
        onMounted(() => {
            this.renderChart();
        });
        onWillUpdateProps((nextProps) => {
            if(this.pieChart){
                this.updateChart(nextProps.data);
            }
        });
        onWillUnmount(() => {
            if(this.pieChart){
                this.pieChart.destroy();
            }
        });
    }

    renderChart() {
        const labels = Object.keys(this.props.data);
        const data = Object.values(this.props.data);
        this.pieChart = new Chart(this.canvasRef.el, {
            type: "pie",
            data: {
                labels: labels,
                datasets: [
                    {
                        label: this.props.label,
                        data: data,
                        backgroundColor: [
                            '#2277B4',
                            '#F97F0F',
                            '#AEC7E8'
                        ],
                        hoverOffset: 4
                    },
                ],
            },
        });
    }

    updateChart(newData) {
        if(this.pieChart){
            this.pieChart.data.labels = Object.keys(newData);
            this.pieChart.data.datasets[0].data = Object.values(newData);
            this.pieChart.update();
        }
    }
}

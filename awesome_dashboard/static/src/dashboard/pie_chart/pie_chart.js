import { Component, onWillStart, useRef, onMounted, onWillUnmount } from "@odoo/owl";
import { loadJS } from '@web/core/assets';

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
    static props = {
        chartLabel: String,
        data: Object,
        colors: Array
    }

    setup() {
        this.pieCanvasRef = useRef("pieCanvas");
        onWillStart(() => loadJS("/web/static/lib/Chart/Chart.js"));
        onMounted(() => this.renderPieChart());
        onWillUnmount(() => {
            if(this.pieChart) {
                this.pieChart.destroy()
            }
        });
    }

    renderPieChart() {
        const dataLabels = Object.keys(this.props.data);
        const dataValues = Object.values(this.props.data);

        this.pieChart = new Chart(this.pieCanvasRef.el, {
            type: 'pie',
            data: {
                labels: dataLabels,
                datasets: [
                    {
                        label: this.props.chartLabel,
                        data: dataValues,
                        backgroundColor: this.props.colors
                    }
                ]
            }
        });
    }
}

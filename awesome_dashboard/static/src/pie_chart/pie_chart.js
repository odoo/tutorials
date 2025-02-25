import { Component, onWillStart, useEffect, useRef, onMounted, onWillUnmount } from '@odoo/owl'
import { loadJS } from "@web/core/assets";


export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
    static props = {
        label: String,
        data: Object,
    }

    setUp() {
        this.canvasRef = useRef("canvas");
        onWillStart(() => loadJS('/web/static/lib/Chart/Chart.js'));

        onMounted(() => {
            console.log("test")
            this.renderChart();
        });
        onWillUnmount(() => {
            this.chart.destroy();
        });
    }

    renderChart() {
        const labels = Object.keys(this.props.data);
        const data = Object.values(this.props.data);
        console.log(data)
        this.chart = new Chart(this.canvasRef.el, {
            type: "pie",
            data: {
                labels: labels,
                datasets: [
                    {
                        label: ["S", "M", "XL"],
                        data: data,
                        backgroundColor: ["#FF6384", "#36A2EB", "#FFCE56",],
                    },
                ],
            },
        });
    }
}

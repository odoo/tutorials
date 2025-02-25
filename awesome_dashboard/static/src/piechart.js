import { Component, useRef, onWillStart, onMounted, onWillUnmount } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component{
    static template = "awesome_dashboard.PieChart";
    static components = [];
    static props = {
        data: Object,
    }

    setup(){
        onWillStart(()=> loadJS("/web/static/lib/Chart/Chart.js"));
        this.canvasRef = useRef("canvas")
        onMounted(() => {
            this.renderChart();
        });
        onWillUnmount(() => {
            this.chart.destroy();
        });
    }

    renderChart(){
        const labels = Object.keys(this.props.data);
        const data = Object.values(this.props.data);
        console.log("Data",data);
        console.log("labels",labels);
        this.chart = new Chart(this.canvasRef.el, {
            type: "pie",
            data: {
                labels: labels,
                datasets: [
                    {
                        data: data,
                    },
                ],
            },
        });
    }
}

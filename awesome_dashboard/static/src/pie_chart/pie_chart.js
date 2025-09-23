import { Component, onMounted, onWillUnmount, onWillStart, useRef } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.pie_chart";
    static props = { data: {optional: false}}

    setup() {
        this.canvasRef = useRef("canvas");
        
        onWillStart(() => loadJS("/web/static/lib/Chart/Chart.js"));
        
        onMounted(() => this.buildChart());

        onWillUnmount(() => this.pieChart.destroy());
    }

    buildChart() {
        this.pieChart = new Chart(this.canvasRef.el, {
            type: "pie",
            data: {
                labels: Object.keys(this.props.data),
                datasets: [{
                        data: Object.values(this.props.data),
                    }],
            },
        });
    }
};

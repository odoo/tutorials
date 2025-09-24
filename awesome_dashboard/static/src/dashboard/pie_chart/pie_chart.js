import { Component, onMounted, onWillUnmount, onWillStart, useEffect, useRef } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.pie_chart";
    static props = { data: {optional: false}}

    setup() {
        this.canvasRef = useRef("canvas");
        
        onWillStart(() => loadJS("/web/static/lib/Chart/Chart.js"));
        
        useEffect(() => {
            if (this.pieChart) {
                this.pieChart.destroy()
            }
            this.data = Object.values(this.props.data.orders_by_size)
            this.labels = Object.keys(this.props.data.orders_by_size)

            this.buildChart()
        });

        onWillUnmount(() => this.pieChart.destroy());
    }

    buildChart() {
        this.pieChart = new Chart(this.canvasRef.el, {
            type: "pie",
            data: {
                labels: this.labels,
                datasets: [{
                        data: this.data,
                    }],
            },
        });
    }
};

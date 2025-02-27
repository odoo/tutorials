
import { loadJS } from "@web/core/assets";
import { Component, onWillStart, onMounted, onWillUnmount, onPatched, useRef } from "@odoo/owl";


export class PieChart extends Component {
    static template = "awesome_dashboard.pie_chart";

    static props = {
        label: { type: String },
        data: { type: Object },
    }

    setup() {
        this.pieChartRef = useRef("pie_chart"); // Récupérer un élément pas encore défini
        

        onWillStart( () => loadJS('/web/static/lib/Chart/Chart.js')); // /web/static/lib/Chart/Chart.js  https://cdn.jsdelivr.net/npm/chart.js

        onMounted(() => {
            this.displayChart();
        });

        onPatched(() => {
            this.chart.destroy();
            this.displayChart();
        });

        onWillUnmount(() => {
            this.chart.destroy();
        });
    }

    displayChart() {
        const labels = Object.keys(this.props.data);
        const values = Object.values(this.props.data);

        this.chart = new Chart(this.pieChartRef.el, {
            type: 'pie',
            data: {
                datasets: [
                    {
                        label: this.props.label,
                        data: values,
                    }
                ],
                labels: labels,
            }
        });     
    }

}


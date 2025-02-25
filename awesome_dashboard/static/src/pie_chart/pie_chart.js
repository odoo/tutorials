
import { loadJs } from "@web/core/assets";
import { Component, useState, onWillStart, useRef } from "@odoo/owl";


export class PieChart extends Component {
    static template = "awesome_dashboard.pie_chart";

    props = {
        label: { type: String },
        data: { type: Array },
        labels: { type: Array },
    }

    setup() {
        this.state = useState({});
        this.myPieChart = useRef("myPieChart"); // Récupérer un élément pas encore défini
        

        onWillStart( () => loadJs(["/web/static/lib/Chart/Chart.js"]));

        onMounted(() => {
            this.displayChart();
        });
    }

    displayChart() {
        new Chart(this.myPieChart.el, {
            type: 'pie_chart',
            data: {
                datasets: [{
                    label: this.props.label,
                    data: this.props.data,
                }],
                labels: this.props.labels,
            }
        });     
    }

}


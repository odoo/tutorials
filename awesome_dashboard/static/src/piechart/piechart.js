import { loadJS } from "@web/core/assets"
import { Component, useState, onWillStart, onMounted, useRef } from "@odoo/owl";

export class Piechart extends Component {
    static template = "awesome_dashboard.piechart";

    static props = {
        pieData: Object
    }

    setup() {
        this.chartRef = useRef("chart")

        this.state = useState({})

        onWillStart(async () => {
            await loadJS("/web/static/lib/Chart/Chart.js")

        })
        onMounted(async () => {
            const ordersBySize = this.props.pieData.orders_by_size
            const data = {
                labels: ["m", "s", "xl"],
                datasets: [{
                    label: "tshirt orders by size",
                    data: [ordersBySize.m, ordersBySize.s, ordersBySize.xl],
                    backgroundColor: [
                    'rgb(255, 99, 132)',
                    'rgb(54, 162, 235)',
                    'rgb(255, 205, 86)'
                    ],
                }],
            }
            const config = {
                type: 'pie',
                data: data,
                };
            
            new Chart(this.chartRef.el, config)
        })

    }
}

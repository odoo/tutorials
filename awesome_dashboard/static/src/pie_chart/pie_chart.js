import { loadJS } from "@web/core/assets";
import { Component, onWillStart, useRef, onMounted } from "@odoo/owl";


export class PieChart extends Component {
    static template = "awesome_owl.pie_chart";

    static props = {
        orders_by_size: {type: Object, shape: {m: Number, s:Number, xl:Number}},
    };

    setup() {
        onWillStart(() => loadJS("/web/static/lib/Chart/Chart.js"));

        this.canvasRef = useRef("canvas");

        onMounted(() => {

            const labels = Object.keys(this.props.orders_by_size);
            const values = Object.values(this.props.orders_by_size);

            new Chart(this.canvasRef.el, {
                type: "pie",
                data: {
                    labels: labels,
                    datasets: [{
                        data: values,
                    }],
                },
            });
        });
    }

}


import {
    Component,
    onWillStart,
    onMounted,
    onWillUnmount,
    useRef,
} from "@odoo/owl";
import { loadJS } from "@web/core/assets";
import { useService } from "@web/core/utils/hooks";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";

    setup() {
        this.canvasRef = useRef("canvas");
        this.statistics = useService("awesome_dashboard.statistics");

        onWillStart(async () => {
            await loadJS("/web/static/lib/Chart/Chart.js");
            this.data = await this.statistics.loadStatistics();
        });

        onMounted(() => {
            const orders = this.data.orders_by_size;

            this.chart = new Chart(this.canvasRef.el, {
                type: "pie",
                data: {
                    labels: ["S", "M", "XL"],
                    datasets: [
                        {
                            data: [
                                orders.m || 0,
                                orders.s || 0,
                                orders.xl || 0,
                            ],
                        },
                    ],
                },
            });
        });

        onWillUnmount(() => {
            this.chart?.destroy();
        });
    }
}

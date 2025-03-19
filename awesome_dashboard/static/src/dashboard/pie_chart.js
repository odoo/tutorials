import { Component, onWillStart, onMounted, xml, reactive } from '@odoo/owl';
import { loadJS } from '@web/core/assets';
import { useService } from '@web/core/utils/hooks';

export class PieChart extends Component {
    static template = xml`
        <canvas class="awesome_dashboard_piechart"></canvas>
    `;
    setup() {
        const statsFetcher = useService('awesome_dashboard.data');
        onWillStart(async () => {
            await loadJS('/web/static/lib/Chart/Chart.js');
            await statsFetcher.loadStatistics();
            this.data = reactive(statsFetcher.getData(), () => this.create());
        });

        onMounted(() => {
            this.create();
        });
    }

    create() {
        if (this.chart) {
            this.chart.destroy();
        }
        const ctx = document.querySelector('.awesome_dashboard_piechart');
        const data = [];
        const labels = [];
        for (const label of Object.keys(this.data.stats.orders_by_size)) {
            data.push(this.data.stats.orders_by_size[label]);
            labels.push(label);
        }
        this.chart = new Chart(ctx, {
            type: 'pie',
            data: {
                datasets: [{ data }],
                labels
            },
            options: {}
        });
    }
}

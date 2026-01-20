import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { reactive } from "@odoo/owl";

const statsMap = {
  average_quantity: { id: 1, title: "Average quanitity order" },
  average_time: { id: 2, title: "Average time for order from new to sent" },
  nb_cancelled_orders: { id: 3, title: "Number of cancelled order this month" },
  nb_new_orders: { id: 4, title: "Number of new orders this month" },
  total_amount: { id: 5, title: "Total amount of new orders" },
};

const statisticService = {
  start() {
    let stats = reactive([]);
    let chartData = reactive({});
    const loadStatistics = async () => {
      const result = await rpc("/awesome_dashboard/statistics");
      const dbItemVisibility = localStorage.getItem("dashboardItemVisibility");
      let formatedres = Object.entries(result).reduce((prev, [key, value]) => {
        const item = statsMap[key];

        if (item) {
          prev.push({
            id: item?.id,
            title: item?.title,
            size: item?.title?.length > 30 ? 2 : 1,
            value,
            isVisible: dbItemVisibility
              ? dbItemVisibility.includes(item?.id)
              : true,
          });
        } else if (typeof value === "object") {
          chartData.labels = Object.keys(value);
          chartData.datasets = [
            {
              label: "Order by size",
              data: Object.values(value),
            },
          ];
          chartData.isVisible = dbItemVisibility
            ? dbItemVisibility.includes("chart")
            : true;
        }
        return prev;
      }, []);

      stats?.push(...formatedres);

      return { stats, chartData };
    };

    loadStatistics();
    
    return {
      stats,
      chartData,
    };
  },
};

registry.category("services").add("load_statistics", statisticService);

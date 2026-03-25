import { NumberCard } from "./number_card/number_card";
import { PieChartCard } from "./pie_chart_card/pie_chart_card";
import { registry } from "@web/core/registry";
import { _t } from "@web/core/l10n/translation";


export const dashboardItemsRegistry = registry.category("awesome_dashboard");

dashboardItemsRegistry.add("average_quantity", {
  id: "average_quantity",
  description: _t("Average amount of t-shirt"),
  Component: NumberCard,
  size: 1,
  props: (data) => ({
    title: _t("Average amount of t-shirt by order this month"),
    value: data.average_quantity || [],
  }),
});

dashboardItemsRegistry.add("average_time", {
  id: "average_time",
  description:
    _t("Average time for an order to go from 'new' to 'sold' or 'cancelled'"),
  Component: NumberCard,
  size: 1.5,
  props: (data) => ({
    title:
      _t("Average time for an order to go from 'new' to 'sold' or 'cancelled'"),
    value: data.average_time || [],
  }),
});

dashboardItemsRegistry.add("nb_new_orders", {
  id: "nb_new_orders",
  description: _t("Number of new orders this month"),
  Component: NumberCard,
  size: 1,
  props: (data) => ({
    title: _t("Number of new orders this month"),
    value: data.nb_new_orders || [],
  }),
});

dashboardItemsRegistry.add("nb_cancelled_orders", {
  id: "nb_cancelled_orders",
  description: _t("Number of cancelled orders this month"),
  Component: NumberCard,
  size: 1,
  props: (data) => ({
    title: _t("Number of cancelled orders this month"),
    value: data.nb_cancelled_orders || [],
  }),
});

dashboardItemsRegistry.add("total_amount", {
  id: "total_amount",
  description: _t("Total amount of new orders this month"),
  Component: NumberCard,
  size: 1,
  props: (data) => ({
    title: _t("Total amount of new orders this month"),
    value: data.total_amount || [],
  }),
});

dashboardItemsRegistry.add("orders_by_size", {
  id: "orders_by_size",
  description: _t("Shirt Orders By Size"),
  Component: PieChartCard,
  size: 2,
  props: (data) => ({
    title: _t("Shirt Orders By Size"),
    values: data.orders_by_size || [],
  }),
});

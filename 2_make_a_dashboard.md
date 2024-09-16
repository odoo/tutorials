# Module 2: Make a Dashboard

It is now time to learn about the Odoo JavaScript framework in its entirety, as
used by the web client. This document is a complete standalone project, in which
we will implement a dashboard client action. It is mostly an excuse to discover
and practice many features of the odoo web framework!

![Overview](_images/overview_02.png)

To get started, you need a running Odoo server and a development environment
setup. Before getting into the exercises, make sure you have a working setup.
Start your odoo server with this repository in the addons path, then install the
`awesome_dashboard` addon.

For this project, we will start from the empty dashboard provided by the
`awesome_dashboard` addon. Then, we will progressively add features to it using
the Odoo JavaScript framework.

Note that a lot of theory is covered in the slides for this event. Also, don't
hesitate to ask questions!

## Content

- [1. A Common Layout](#1-a-common-layout)
- [2. Add some buttons for quick navigation](#2-add-some-buttons-for-quick-navigation)
- [3. Add a dashboard item](#3-add-a-dashboard-item)
- [4. Call the server, add some statistics](#4-call-the-server-add-some-statistics)
- [5. Cache network calls, create a service](#5-cache-network-calls-create-a-service)
- [6. Display a pie chart](#6-display-a-pie-chart)
- [7. Periodic Updates](#7-periodic-updates)
- [8. Lazy loading the dashboard](#8-lazy-loading-the-dashboard)
- [9. Making our dashboard generic](#9-making-our-dashboard-generic)
- [10. Making our dashboard extensible](#10-making-our-dashboard-extensible)
- [11. Add and remove dashboard items](#11-add-and-remove-dashboard-items)
- [12. Going further](#12-going-further)

## 1. A Common Layout

Most screens in the Odoo web client uses a common layout: a control panel on
top, with some buttons, and a main content zone just below. This is done using
the `Layout` component, available in `@web/search/layout`.

1. Update the `AwesomeDashboard` component located in
   `awesome_dashboard/static/src/` to use the `Layout` component. You can use
   `{controlPanel: {} }` for the display props of the `Layout` component.
2. Add a className prop to `Layout`: `className="'o_dashboard h-100'"`
3. Add a `dashboard.scss` file in which you set the `background-color` of
   .`o_dashboard` to gray (or your favorite color)
4. Open http://localhost:8069/odoo, then open the Awesome Dashboard app, and see
   the result.

![Layout component](_images/new_layout.png)

#### See also

- Example:
  [use of Layout in client action](https://github.com/odoo/odoo/blob/master/addons/web/static/src/webclient/actions/reports/report_action.js)
  and
  [template](https://github.com/odoo/odoo/blob/master/addons/web/static/src/webclient/actions/reports/report_action.xml)
- Example:
  [use of Layout in kanban views](https://github.com/odoo/odoo/blob/master/addons/web/static/src/views/kanban/kanban_controller.xml)

## 2. Add some buttons for quick navigation

One important service provided by Odoo is the `action` service: it can execute
all kind of standard actions defined by Odoo. For example, here is how one
component could execute an action by its xml id:

```js
import { useService } from "@web/core/utils/hooks";
...
setup() {
      this.action = useService("action");
}
openSettings() {
      this.action.doAction("base_setup.action_general_configuration");
}
...
```

Let us now add two buttons to our control panel:

1. A button `Customers`, which opens a kanban view with all customers (this
   action already exists, so you should use its
   [xml id](https://github.com/odoo/odoo/blob/1f4e583ba20a01f4c44b0a4ada42c4d3bb074273/odoo/addons/base/views/res_partner_views.xml#L510)).
2. A button `Leads`, which opens a dynamic action on the `crm.lead` model with a
   list and a form view. Follow the example of
   [this use of the action service](https://github.com/odoo/odoo/blob/ef424a9dc22a5abbe7b0a6eff61cf113826f04c0/addons/account/static/src/components/journal_dashboard_activity/journal_dashboard_activity.js#L28-L35).

![Navigation buttons](_images/navigation_buttons.png)

**See also:**
[code: action service](https://github.com/odoo/odoo/blob/master/addons/web/static/src/webclient/actions/action_service.js)

## 3. Add a dashboard item

Let us now improve the content of this dashboard.

1. Create a generic `DashboardItem` component that display its default slot in a
   nice card layout. It should take an optional `size` number props, that
   default to 1. The width should be hardcoded to `(18*size)rem`.
2. Add two cards to the dashboard. One with no size, and the other with a size
   of 2.

![Dashboard items](_images/dashboard_item.png)

**See also:**
[Owl slot system](https://github.com/odoo/owl/blob/master/doc/reference/slots.md)

## 4. Call the server, add some statistics

Let’s improve the dashboard by adding a few dashboard items to display real
business data. The `awesome_dashboard` addon provides a
`/awesome_dashboard/statistics` route that is meant to return some interesting
information.

To call a specific controller, we need to use the `rpc` function. This function
`rpc(route, params, settings)` is the low level communication code that will
create a network request to the server in jsonrpc, then will return a promise
with the result. A basic request could look like this:

```js
import { rpc } from "@web/core/network/rpc";
...
setup() {
      onWillStart(async () => {
         const result = await rpc("/my/controller", {a: 1, b: 2});
         // ...
      });
}
...
```

1. Update Dashboard so that it uses the `rpc` function.
2. Call the statistics route `/awesome_dashboard/statistics` in the
   `onWillStart` hook.
3. Display a few cards in the dashboard containing:
   - Number of new orders this month
   - Total amount of new orders this month
   - Average amount of t-shirt by order this month
   - Number of cancelled orders this month
   - Average time for an order to go from ‘new’ to ‘sent’ or ‘cancelled’

![Statistics](_images/statistics1.png)

## 5. Cache network calls, create a service

If you open the Network tab of your browser’s dev tools, you will see that the
call to `/awesome_dashboard/statistics` is done every time the client action is
displayed. This is because the `onWillStart` hook is called each time the
`Dashboard` component is mounted. But in this case, we would prefer to do it
only the first time, so we actually need to maintain some state outside of the
`Dashboard` component. This is a nice use case for a service!

1. Register and import a `new awesome_dashboard.statistics` service.
2. It should provide a function `loadStatistics` that, once called, performs the
   actual rpc, and always return the same information.
3. Use the `memoize` utility function from `@web/core/utils/functions` that
   allows caching the statistics.
4. Use this service in the `Dashboard` component.
5. Check that it works as expected.

#### See also

- [Example: simple service](https://github.com/odoo/odoo/blob/master/addons/web/static/src/core/network/http_service.js)
- [Example: service with a dependency](https://github.com/odoo/odoo/blob/master/addons/web/static/src/core/network/http_service.js)

## 6. Display a pie chart

Everyone likes charts (!), so let us add a pie chart in our dashboard. It will
display the proportions of t-shirts sold for each size: S/M/L/XL/XXL.

For this exercise, we will use [Chart.js](https://www.chartjs.org/). It is the
chart library used by the graph view. However, it is not loaded by default, so
we will need to either add it to our assets bundle, or lazy load it. Lazy
loading is usually better since our users will not have to load the chartjs code
every time if they don’t need it.

1.  Create a `PieChart` component.
2.  In its `onWillStart` method, load chartjs, you can use the
    [loadJs function](https://github.com/odoo/odoo/blob/1f4e583ba20a01f4c44b0a4ada42c4d3bb074273/addons/web/static/src/core/assets.js#L23)
    to load `/web/static/lib/Chart/Chart.js`.
3.  Use the `PieChart` component in a `DashboardItem` to display a
    [pie chart](https://www.chartjs.org/docs/2.8.0/charts/doughnut.html) that
    shows the quantity for each sold t-shirts in each size (that information is
    available in the `/statistics` route). Note that you can use the size
    property to make it look larger.
4.  The `PieChart` component will need to render a canvas, and draw on it using
    chart.js. You can use this code to create the pie chart:

        ```js
            import { getColor } from "@web/core/colors/colors";
            ...
            renderChart() {
                const labels = Object.keys(this.props.data);
                const data = Object.values(this.props.data);
                const color = labels.map((_, index) => getColor(index));
                this.chart = new Chart(this.canvasRef.el, {
                    type: "pie",
                    data: {
                        labels: labels,
                        datasets: [
                            {
                                label: this.props.label,
                                data: data,
                                backgroundColor: color,
                            },
                        ],
                    },
                });
            }
        ```

5.  Make it work!

![Pie Chart](_images/pie_chart.png)

#### See also

- Example:
  [lazy loading a js file](https://github.com/odoo/odoo/blob/1f4e583ba20a01f4c44b0a4ada42c4d3bb074273/addons/web/static/src/views/graph/graph_renderer.js#L57)
- Example:
  [rendering a chart in a component](https://github.com/odoo/odoo/blob/1f4e583ba20a01f4c44b0a4ada42c4d3bb074273/addons/web/static/src/views/graph/graph_renderer.js#L618)

## 7. Periodic Updates

Since we moved the data loading in a cache, it never updates. But let us say
that we are looking at fast moving data, so we want to periodically (for
example, every 10min) reload fresh data.

This is quite simple to implement, with a `setTimeout` or `setInterval` in the
statistics service. However, here is the tricky part: if the dashboard is
currently being displayed, it should be updated immediately.

To do that, one can use a `reactive` object: it is just like the proxy returned
by `useState`, but not linked to any component. A component can then do a
`useState` on it to subscribe to its changes.

1. Update the statistics service to reload data every 10 minutes (to test it,
   use 10s instead!)
2. Modify it to return a
   [reactive](https://github.com/odoo/owl/blob/master/doc/reference/reactivity.md#reactive)
   object. Reloading data should update the reactive object in place.
3. Update the `Dashboard` component to wrap the reactive object in a `useState`

#### See also

- [Documentation on reactivity](https://github.com/odoo/owl/blob/master/doc/reference/reactivity.md)
- [Example: Use of reactive in a service](https://github.com/odoo/odoo/blob/1f4e583ba20a01f4c44b0a4ada42c4d3bb074273/addons/web/static/src/core/debug/profiling/profiling_service.js#L30)

## 8. Lazy loading the dashboard

Let us imagine that our dashboard is getting quite big, and is only of interest
to some of our users. In that case, it could make sense to lazy load our
dashboard, and all related assets, so we only pay the cost of loading the code
when we actually want to look at it.

One way to do this is to use `LazyComponent` (from @web/core/assets) as an
intermediate that will load an asset bundle before displaying our component.

For example, it can be used like this:

```js
export class ExampleComponentLoader extends Component {
  static components = { LazyComponent };
  static template = xml`
        <LazyComponent bundle="'example_module.example_assets'" Component="'ExampleComponent'" />
    `;
}

registry
  .category("actions")
  .add("example_module.example_action", ExampleComponentLoader);
```

1. Move all dashboard assets into a sub folder `/dashboard` to make it easier to
   add to a bundle.
2. Create a `awesome_dashboard.dashboard` assets bundle containing all content
   of the `/dashboard` folder.
3. Modify `dashboard.js` to register itself to the `lazy_components` registry
   instead of `actions`.
4. In `src/dashboard_action.js`, create an intermediate component that uses
   `LazyComponent` and register it to the `actions` registry.

## 9. Making our dashboard generic

So far, we have a nice working dashboard. But it is currently hardcoded in the
dashboard template. What if we want to customize our dashboard? Maybe some users
have different needs and want to see other data.

So, the next step is to make our dashboard generic: instead of hard-coding its
content in the template, it can just iterate over a list of dashboard items. But
then, many questions come up: how to represent a dashboard item, how to register
it, what data should it receive, and so on. There are many different ways to
design such a system, with different trade-offs.

For this tutorial, we will say that a dashboard item is an object with the
following structure:

```js
const item = {
  id: "average_quantity",
  description: "Average amount of t-shirt",
  Component: StandardItem,
  // size and props are optionals
  size: 3,
  props: (data) => ({
    title: "Average amount of t-shirt by order this month",
    value: data.average_quantity,
  }),
};
```

The `description` value will be useful in a later exercise to show the name of
items that the user can add to their dashboard. The `size` number is optional,
and simply describes the size of the dashboard item that will be displayed.
Finally, the `props` function is optional. If not given, we will simply give the
`statistics` object as data. But if it is defined, it will be used to compute
specific props for the component.

The goal is to replace the content of the dashboard with something that look
like the following snippet:

```xml
<t t-foreach="items" t-as="item" t-key="item.id">
   <DashboardItem size="item.size || 1">
      <t t-set="itemProp" t-value="item.props ? item.props(statistics) : {'data': statistics}"/>
      <t t-component="item.Component" t-props="itemProp" />
   </DashboardItem>
</t>
```

Note that the above example features two advanced features of Owl: dynamic
components and dynamic props.

We currently have two kinds of item components: number cards with a title and a
number, and pie cards with some label and a pie chart.

1.  Create and implement two components: `NumberCard` and `PieChartCard`, with
    the corresponding props.
2.  Create a file `dashboard_items.js` in which you define and export a list of
    items, using `NumberCard` and `PieChartCard` to recreate our current
    dashboard.
3.  Import that list of items in our `Dashboard` component, add it to the
    component, and update the template to use a `t-foreach` like shown above.

        ```js
        setup() {
        this.items = items;
        }
        ```

And now, our dashboard template is generic!

## 10. Making our dashboard extensible

However, the content of our item list is still hardcoded. Let us fix that by
using a registry:

1. Instead of exporting a list, register all dashboard items in a
   `awesome_dashboard` registry
2. Import all the items of the `awesome_dashboard` registry in the `Dashboard`
   component

The dashboard is now easily extensible. Any other Odoo addon that wants to
register a new item to the dashboard can just add it to the registry.

## 11. Add and remove dashboard items

Let us see how we can make our dashboard customizable. To make it simple, we
will save the user dashboard configuration in the local storage, so that we
don’t have to deal with the server for now.

For this exercise, the dashboard configuration will be saved as a list of
removed item ids.

1. Add a button in the control panel with a gear icon to indicate that it is a
   settings button.
2. Clicking on that button should open a dialog.
3. In that dialog, we want to see a list of all existing dashboard items, each
   with a checkbox.
4. There should be a Apply button in the footer. Clicking on it will build a
   list of all item ids that are unchecked.
5. We want to store that value in the local storage.
6. And modify the Dashboard component to filter the current items by removing
   the ids of items from the configuration.

![Item configurations](_images/items_configuration.png)

## 12. Going further

Here is a list of some small (and not so small) improvements you could try to do
if you have the time:

- Make sure your application can be translated (with `_t`).
- Clicking on a section of the pie chart should open a list view of all orders
  that have the corresponding size.
- Save the content of the dashboard in a user setting on the server!
- Make it responsive: in mobile mode, each card should take 100% of the width.
- Update the dashboard in real time by using the bus (hard)

import { registry } from "@web/core/registry";


const numbers = [
    {
        title: 'Some title.',
        value: 103,
    },
    {
        title: 'Some other title.',
        value: 418,
    },
    {
        title: 'Average Quantity',
        source: 'average_quantity',
    },
    {
        title: 'Average Time',
        source: 'average_time',
    },
    {
        title: 'Number of Cancelled Orders',
        source: 'nb_cancelled_orders',
    },
    {
        title: 'Number of New Orders',
        source: 'nb_new_orders',
    },
    {
        title: 'Total Amount',
        source: 'total_amount',
    },
];

registry.category('awesome_dashboard.data').add('numbers', numbers);

const graphs = [
    {
        id: 'graph1',
        title: 'An graph.',
        data: {
            value1: 9,
            value2: 3,
            value3: 9,
        },
    },
    {
        id: 'graph2',
        title: 'Another graph.',
        data: {
            'Jean-Eud le Tacos Vegan': 1536,
            'Bérénice la Saucisse Créatrice': 32,
            'Monsieur Puel Monsieur': 3,
        },
    },
    {
        id: 'shirt_size_pie',
        title: 'T-Shirt Sales by Size',
        source: 'orders_by_size',
    },
];

registry.category('awesome_dashboard.data').add('graphs', graphs);

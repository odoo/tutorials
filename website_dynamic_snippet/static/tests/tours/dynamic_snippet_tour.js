import {
    clickOnSnippet,
    registerWebsitePreviewTour,
} from '@website/js/tours/tour_utils';

registerWebsitePreviewTour('website_dynamic_snippet.sale_order_snippet', {
    url: '/',
    edition: true,
},
    () => {
        return [
        {
            content: "Drag and drop the sale order snippet",
            trigger: "[data-snippet='sale_order_highlight']",
            run: "drag_and_drop :iframe #wrap .oe_drop_zone"
        },
        ...clickOnSnippet({ id: "categories_section", name:"Sale Order Snippet" }),
        {
            content: "Click on the layout change Option",
            trigger: "[data-name='snippet_data_view']",
            run: "click"
        },
        {
            content: "Change layout to list",
            trigger: "[data-set-layout='list']",
            run: "click"
        },
        {
            content: "Check if layout is list",
            trigger: ":iframe .categories_section[data-set-layout='list']",
        },
        {
            content: "Click on the layout change Option",
            trigger: "[data-name='snippet_data_view']",
            run: "click"
        },
        {
            content: "Change layout to grid",
            trigger: "[data-set-layout='grid']",
            run: "click"
        },
        {
            content: "Check if layout is grid",
            trigger: ":iframe .categories_section[data-set-layout='grid']",
        },
        {
            content: "Click on the confirm order only Option",
            trigger: "[data-confirm-order-only='true'] we-checkbox",
            run: "click"
        },
        {
            content: "Save the snippet",
            trigger: "[data-action='save']",
            run: "click"
        },
        ]
    }
)

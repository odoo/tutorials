import {
    changeOption,
    insertSnippet,
    clickOnSnippet,
    clickOnEditAndWaitEditMode,
    clickOnSave,
    registerWebsitePreviewTour,
} from '@website/js/tours/tour_utils';

function helpdeskSnippetTourSteps() {
    return [
        ...clickOnEditAndWaitEditMode(),
        {
            content: "Click on the Helpdesk snippet to insert it.",
            trigger: "[data-snippet='s_helpdesk_tickets']",
            run: "drag_and_drop :iframe #wrap .oe_drop_zone",
        },
        ...clickOnSnippet({ id: "categories_section", name: "Helpdesk Ticket" }),
        {
            content: "Click to open the layout selection.",
            trigger: '[data-option-name="view_template"] we-toggler',
            run: 'click',
        },
        {
            content: "Select the card layout.",
            trigger: '[data-select-layout="card"]',
            run: 'click',
        },
        {
            content: "check that list to card layout is selected",
            trigger: ":iframe .categories_section[data-layout='card']",
        },
        {
            content: "Open the Helpdesk Team filter.",
            trigger: '[data-name="helpdesk_team_opt"] we-toggler',
            run: 'click',
        },
        {
            content: "Choose a Helpdesk Team to filter the tickets.",
            trigger: '[data-select-data-attribute="2"]',
            run: 'click',
        },
        {
            content: "check that my team id-2 filter apply",
            trigger: ':iframe .categories_section[data-helpdesk-team-id="2"]',
        },
        ...clickOnSave(),
    ];
}

registerWebsitePreviewTour(
    "website_helpdesk_snippet.helpdesk_snippet_tour", // same name as your js tour name
    {
        url: "/", // staring point of my url
    },
    helpdeskSnippetTourSteps
);

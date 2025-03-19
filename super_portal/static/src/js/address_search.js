/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

function filterAddresses(inputElement, sectionClass) {
    let searchTerm = inputElement.value.toLowerCase();
    let addressTiles = document.querySelectorAll(`.${sectionClass} .one_kanban`);

    addressTiles.forEach((tile) => {
        let textContent = tile.innerText.toLowerCase();
        let isSelected = tile.querySelector('.card')?.classList.contains('bg-primary');

        tile.style.display = textContent.includes(searchTerm) || isSelected ? 'block' : 'none';
    });
}
window.filterAddresses = filterAddresses;

publicWidget.registry.AddressSearch = publicWidget.Widget.extend({
    selector: '.o_billing_address_search, .o_shipping_address_search',

    events: {
        'keyup .o_billing_address_search': '_onKeyUpBilling',
        'keyup .o_shipping_address_search': '_onKeyUpShipping',
    },

    _onKeyUpBilling: function (ev) {
        filterAddresses(ev.currentTarget, 'all_billing');
    },

    _onKeyUpShipping: function (ev) {
        filterAddresses(ev.currentTarget, 'all_shipping');
    },
});

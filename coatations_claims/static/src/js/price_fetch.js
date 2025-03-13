import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from '@web/core/network/rpc';

publicWidget.registry.WebsiteSale.include({
    events: {
        'click #get_price_button': '_onGetPriceClick',  // Attach event to the Get Price button
        'change #price_select': '_onPriceSelectChange', // Add event listener for dropdown change
    },

    _onGetPriceClick: async function (ev) {
        ev.preventDefault();
        
        const productId = this.$el.find("input[name='product_id']").val();  // Assuming product ID is stored in input field

        if (!productId) {
            console.error("Product ID is missing");
            return;
        }

        try {
            // Fetch coatation options for the product
            const result = await rpc('/coatations_claims/get_product_options', { product_id: productId });

            if (result.error) {
                console.error("Error fetching price options:", result.error);
                return;
            }

            const options = result.options;
            if (options.length === 0) {
                console.log("No price options available.");
                return;
            }

            // Create the <select> options dynamically
            let optionsHtml = '';
            options.forEach(option => {
                const optionText = `${option.coatation_id} - ${option.client_name} - $${option.price}`;
                optionsHtml += `<option value="${option.coatation_id}|${option.client_name}|${option.price}">${optionText}</option>`;
            });

            // Populate the dropdown
            this.$el.find('#price_select').html(optionsHtml);

        } catch (error) {
            console.error("Error fetching price options:", error);
        }
    },

    _onPriceSelectChange: function (ev) {
        const selectedOption = this.$el.find('#price_select').val();
        
        if (!selectedOption) {
            return;
        }

        // The selected value is in the format: Coatation_ID|Client_Name|Price
        const selectedPriceDetails = selectedOption.split('|');
        const selectedPrice = selectedPriceDetails[2];  // The price is the 3rd value

        // Update the price element with the new price
        this._updateMainPrice(selectedPrice);
    },

    _updateMainPrice: function (newPrice) {
        // Find the element with the class 'oe_currency_value' and update its content
        const priceElement = this.$el.find('.oe_currency_value');
        
        if (priceElement.length > 0) {
            // Update the price displayed on the page
            priceElement.text(newPrice);
        }
    }
});

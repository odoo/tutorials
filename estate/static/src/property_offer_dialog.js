document.addEventListener("DOMContentLoaded", function () {
    document.body.addEventListener("click", function (event) {
        const button = event.target.closest("#make_offer_primary_button")

        if (!button) return;

        const modalPropertyId = document.getElementById("modal-property-id");

        if (!modalPropertyId) {
            console.error("Modal input elements not found!");
            return;
        }

        const propertyId = button.getAttribute("data-property-id");

        if (!propertyId) {
            console.error("Property ID or User ID not found in button attributes!");
            return;
        }

        modalPropertyId.value = propertyId;
    });
});

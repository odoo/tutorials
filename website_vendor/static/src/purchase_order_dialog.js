document.addEventListener("DOMContentLoaded", function () {
    let vendorQtyMap = {};
    let vendorPriceMap = {};
    document.body.addEventListener("click", function (event) {
        const button = event.target.closest(".create-po-btn");
        if (!button) return;

        const modalProductId = document.getElementById("modal-product-id");
        const modalProductName = document.getElementById("modal-product-name");
        const modalProductPrice = document.getElementById("modal-product-price");
        const vendorSelect = document.getElementById("vendor_select");
        const modalProductQty = document.getElementById("modal-product-qty")

        const productId = button.getAttribute("data-product-id");
        const productName = button.getAttribute("data-product-name");
        const productPrice = button.getAttribute("data-product-price");
        const productVendors = button.getAttribute("data-product-vendors");

        modalProductId.value = productId;
        modalProductName.textContent = productName;
        modalProductPrice.textContent = productPrice;
        vendorQtyMap = {};
        vendorPriceMap = {};

        vendorSelect.innerHTML = '<option value="">Choose Vendor</option>';

        if (!productVendors) {
            console.error("No vendor data found!");
            return;
        }

        try {
            const decodedData = productVendors.replace(/&quot;/g, '"');
            const jsonArray = JSON.parse(decodedData);

            jsonArray.forEach(vendor => {
                const option = new Option(vendor.vendor_name, vendor.vendor_id)
                vendorSelect.add(option)
                vendorQtyMap[vendor.vendor_id] = Number(vendor.min_qty);
                vendorPriceMap[vendor.vendor_id] = Number(vendor.price);
            });
        } catch (error) {
            console.error("Error parsing JSON: ", error);
        }

        vendorSelect.addEventListener("change", function () {
            const selectedVendorId = this.value;
            if (selectedVendorId) {
                modalProductQty.value = vendorQtyMap[selectedVendorId];
                modalProductPrice.textContent = `$ ${vendorPriceMap[selectedVendorId]}`;
            }
        });

        modalProductQty.addEventListener("change", function () {
            const selectedVendorId = document.getElementById("vendor_select").value;
            if (!selectedVendorId) {
                alert("Please select a vendor first.");
                this.value = "";
                return;
            }
        
            const minQty = vendorQtyMap[selectedVendorId];
            const enteredQty = Number(this.value);
        
            if (enteredQty < minQty) {
                const userConfirmed = confirm(
                    `Minimum quantity required for this vendor is ${minQty}.
                     Do you want to update the quantity?`
                );
                if (userConfirmed) {
                    this.value = minQty;
                } else {
                    this.value = "";
                }
            } else if ((enteredQty % minQty) !== 0) {
                const userConfirmed = confirm(
                    `Quantity should be a multiple of ${minQty} for this vendor. 
                     Do you want to update the quantity?`
                );
                if (userConfirmed == true) {
                    this.value = minQty;
                } else {
                    this.value = "";
                }
            }
        });
        
    });
});
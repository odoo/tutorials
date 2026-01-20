import { rpc } from "@web/core/network/rpc";

async function update_all_bids() {
    const bid_data = [...document.querySelectorAll(".bid-qty")]
        .map(input => {
            const line_id = input.dataset.lineId;
            return {
                order_id: parseInt(input.dataset.orderId),
                line_id: parseInt(line_id),
                bid_qty: parseFloat(input.value) || 0,
                bid_price: parseFloat(
                    document.querySelector(`.bid-price[data-line-id="${line_id}"]`)?.value || "0"
                )
            };
        })
        .filter(bid => bid.bid_qty > 0 && bid.bid_price > 0);

    if (bid_data.length === 0) {
        alert("No valid bids to update!");
        return;
    }
    try {
        const response = await rpc("/update_bids", { bids: bid_data });
        if (response.success) {
            alert("Bids updated successfully!");
            location.reload();
        } else {
            alert("Error updating bids.");
        }
    } catch (error) {
        alert("Failed to update bids.");
    }
}

function onClick() {
    const button = document.getElementById("update_all_bids");
    if (button) {
        button.addEventListener("click", update_all_bids);
    }
}

onClick();

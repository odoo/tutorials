document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("offerForm").addEventListener("submit", function (event) {
        event.preventDefault();  

        let propertyId = document.getElementById("propertyId").value.trim();
        let offerPrice = document.getElementById("offerPrice").value.trim();
        let validityDays = document.getElementById("validityDays").value.trim();
        let userName = document.getElementById("userName").value.trim();
        let userEmail = document.getElementById("userEmail").value.trim();
        let userIdElement = document.getElementById("userId");
        let userId = userIdElement ? userIdElement.value.trim() : null;

        if (!propertyId || !offerPrice || !validityDays || !userName || !userEmail) {
            alert("Please fill in all required fields.");
            return;
        }

        fetch('/create_offer', {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                property_id: propertyId,
                offer_price: offerPrice,
                validity_days: validityDays,
                user_name: userName,
                user_email: userEmail,
                user_id: userId
            })
        }).then(response => response.json())
          .then(data => {
              if (data.success) {
                  alert("Offer submitted successfully!");
                  window.location.reload();
              } else {
                  alert("Error submitting offer: " + data.error);
              }
          }).catch(error => console.error("Error:", error));
    });
});

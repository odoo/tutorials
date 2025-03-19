document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("offerForm").addEventListener("submit", function (event) {
        event.preventDefault();

        let propertyId = document.getElementById("propertyId").value;
        let offerPrice = document.getElementById("offerPrice").value;
        let validityDays = document.getElementById("validityDays");
        let userContact = document.getElementById("userContact").value;
        let userName = document.getElementById("userName").value;
        let userEmail = document.getElementById("userEmail").value;
        let userId = document.getElementById("userId").value;
        
        offerData = {
            propertyId: propertyId,
            offerPrice: offerPrice,
            validityDays: validityDays,
            userContact: userContact,
            userName: userName,
            userEmail: userEmail,
            userId: userId
        }


    });
});
import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.CountdownTimer = publicWidget.Widget.extend({
  selector: "#auction_timer",
  start: function () {
    var timer = document.getElementById("auction_timer");
    var endTimeStr = timer.getAttribute("data-end-time");

    if (!endTimeStr) {
      timer.textContent = "No auction end time set";
      return;
    }

    var endTime = new Date(endTimeStr + "Z").getTime(); // Force UTC parsing

    if (isNaN(endTime)) {
      timer.textContent = "Invalid end time";
      return;
    }

    function updateTimer() {
      var now = Date.now();
      var timeLeft = endTime - now;

      if (timeLeft > 0) {
        var days = Math.floor(timeLeft / (1000 * 60 * 60 * 24));
        var hours = Math.floor(
          (timeLeft % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)
        );
        var minutes = Math.floor((timeLeft % (1000 * 60 * 60)) / (1000 * 60));
        var seconds = Math.floor((timeLeft % (1000 * 60)) / 1000);

        timer.textContent = `${days}d ${hours}h ${minutes}m ${seconds}s`;
      } else {
        timer.textContent = "Auction Ended";
        clearInterval(interval);
      }
    }

    updateTimer();
    var interval = setInterval(updateTimer, 1000);
  },
});

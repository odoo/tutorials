const countdown = document.getElementById("auction_countdown");
if (countdown) {
    const endTime = new Date( countdown.dataset.endTime).getTime();

    function updateCountdown() {
        const now = new Date().getTime();
        const distance = endTime - now;

        if (distance <= 0) {
            countdown.innerHTML = "00d 00h 00m 00s";
            return;
        }

        const days =
            Math.floor(
                distance / (1000 * 60 * 60 * 24)
            );

        const hours =
            Math.floor(
                (
                    distance %
                    (1000 * 60 * 60 * 24)
                )
                /
                (1000 * 60 * 60)
            );

        const minutes =
            Math.floor(
                (
                    distance %
                    (1000 * 60 * 60)
                )
                /
                (1000 * 60)
            );

        const seconds =
            Math.floor(
                (
                    distance %
                    (1000 * 60)
                )
                /
                1000
            );

        countdown.innerHTML =
            days + "d "
            +
            hours + "h "
            +
            minutes + "m "
            +
            seconds + "s";
    }

    updateCountdown();

    setInterval(
        updateCountdown,
        1000
    );
}

cards = document.querySelectorAll(".card");

// if card is hovered,play the video in the card else pause the video
cards.forEach((card) => {
    card.addEventListener("mouseover", () => {
        card.querySelector("video").play();
    });
    card.addEventListener("mouseout", () => {
        // reset the video to the start
        card.querySelector("video").currentTime = 0;
        card.querySelector("video").pause();
    });
});

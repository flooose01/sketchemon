"use strict";

(function () {
  let drawing = false;
  let cleared = true;
  let context;
  let canvas;

  window.addEventListener("load", init);

  function init() {
    canvas = document.getElementById("sketchCanvas");
    canvas.height = screen.height * 0.6;
    canvas.width = screen.height * 0.6;
    context = canvas.getContext("2d");
    drawing = false;

    canvas.addEventListener("mousedown", () => {
      drawing = true;
      cleared = false;
    });

    canvas.addEventListener("mouseup", () => {
      drawing = false;
      cleared = false;
      context.beginPath();
    });

    canvas.addEventListener("mousemove", draw);

    canvas.addEventListener("touchstart", (e) => {
      e.preventDefault();
      startPosition(e);
    });
    canvas.addEventListener("touchend", (e) => {
      e.preventDefault();
      endPosition();
    });
    canvas.addEventListener("touchmove", (e) => {
      e.preventDefault();
      draw(e);
    });

    document.getElementById("genButton").addEventListener("click", () => {
      const dataURL = canvas.toDataURL("image/png");
      const series = parseInt(document.getElementById("evolInput").value) + 1;
      let statusMsg = document.getElementById("statusMsg");
      statusMsg.textContent = "Generating...";
      let payload;
      if (cleared) {
        payload = JSON.stringify({ img_provided: false, series: series });
      } else {
        payload = JSON.stringify({
          img_provided: true,
          image: dataURL,
          series: series,
        });
      }

      fetch("/generate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: payload,
      })
        .then(checkStatus)
        .then((response) => response.json())
        .then((data) => {
          document.getElementById("statusMsg").textContent = "";

          // Remove the existing image first
          let div = document.getElementById("images");
          while (div.firstChild) {
            div.removeChild(div.firstChild);
          }

          let cards = data["cards"];
          let pokemons = data["pokemons"];

          for (let i = 0; i < cards.length; i++) {
            let card = cards[i];
            let pokemon = pokemons[i];
            addPokemon(card, pokemon);
          }
        });
    });

    document.getElementById("clearButton").addEventListener("click", () => {
      context.clearRect(0, 0, canvas.width, canvas.height);
      cleared = true;
    });
  }

  function startPosition(e) {
    drawing = true;
    draw(e);
  }

  function endPosition() {
    drawing = false;
    context.beginPath();
  }

  function addPokemon(card, pokemon) {
    const imagesDiv = document.getElementById("images");
    let cardImg = "data:image/png;base64, " + card;

    let res = document.createElement("div");
    res.className = "pokemon-container";

    let div1 = document.createElement("div");
    div1.className = "image-container";

    let div2 = document.createElement("div");
    div2.className = "description-container";

    let img1 = document.createElement("img");
    img1.src = cardImg;
    img1.className = "pokemon-image";

    let h2 = document.createElement("h2");
    h2.className = "pokemon-name";
    h2.textContent = pokemon.name;
    let p = document.createElement("p");
    p.className = "pokemon-description";
    p.textContent = pokemon.description;

    div1.appendChild(img1);
    div2.appendChild(h2);
    div2.appendChild(p);

    res.appendChild(div1);
    res.appendChild(div2);

    imagesDiv.appendChild(res);
  }

  function draw(e) {
    if (!drawing) return;
    cleared = false;
    context.lineWidth = 5;
    context.lineCap = "round";
    context.strokeStyle = "black";

    let x, y;

    if (e.type === "mousemove") {
      x = e.clientX - canvas.offsetLeft;
      y = e.clientY - canvas.offsetTop;
    } else if (e.type === "touchmove") {
      const touch = e.touches[0];
      x = touch.clientX - canvas.offsetLeft;
      y = touch.clientY - canvas.offsetTop;
    }

    context.lineTo(x, y);
    context.stroke();
    context.beginPath();
    context.moveTo(x, y);
  }

  async function checkStatus(res) {
    if (!res.ok) {
      document.getElementById("statusMsg").textContent = "Failed to generate. Try again!";
      throw new Error(await res.text());
    }
    return res;
  }
})();


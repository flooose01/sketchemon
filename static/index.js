"use strict";

(function () {
  let drawing = false;
  let cleared = true;
  let context;
  let canvas;

  window.addEventListener("load", init);

  function init() {
    canvas = document.getElementById("sketchCanvas");
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

    document.getElementById("genButton").addEventListener("click", () => {
      const dataURL = canvas.toDataURL("image/png");
      const series = parseInt(document.getElementById("evolInput").value) + 1;

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
      // context.clearRect(0, 0, canvas.width, canvas.height);
      // cleared = true;
      let card = canvas.toDataURL("image/png");
      let pokemon = {
        name: "ember",
        description:
          "tthaas idbfanjsdfbk asd bfk asbdfkj asbdfkjasb dfk jabsdkjfbakjsbdfj asdbfkjasdbfkja bsdkjfb akjsdbf kjasbdf kjasbdfkj asdkf bkasdf a",
      };
      addPokemon(card, pokemon);
    });
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

  function draw(event) {
    if (!drawing) return;
    cleared = false;
    context.lineWidth = 5;
    context.lineCap = "round";
    context.strokeStyle = "black";

    context.lineTo(
      event.clientX - canvas.offsetLeft,
      event.clientY - canvas.offsetTop
    );
    context.stroke();
    context.beginPath();
    context.moveTo(
      event.clientX - canvas.offsetLeft,
      event.clientY - canvas.offsetTop
    );
  }

  async function checkStatus(res) {
    if (!res.ok) {
      throw new Error(await res.text());
    }
    return res;
  }
})();

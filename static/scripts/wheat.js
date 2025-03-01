let form = document.getElementById("form");
let result = document.getElementById("result");
let loader = document.getElementById("loader");
let fields_load = document.getElementById("fields-load");

// ignore the target attribute
ignore_list = ["Type"];
custom_label = {};

fetch("/predict/wheat-type", {
    method: "POST",
    headers: {
        "Content-Type": "application/json",
    },
})
    .then((response) => response.json())
    .then((data) => {
        console.log("Fields details fetched successfully", data);
        fields_load.style.display = "none";
        create_fields(data, form, ignore_list, custom_label);
    })
    .catch((error) => {
        console.error("Error:", error);
        alert("Error occurred. Please try again.");
    });

form.addEventListener("submit", (event) => {
    event.preventDefault();

    if (validateForm(form) === false) {
        return;
    }

    // disable the submit button
    form.querySelector("input[type=submit]").disabled = true;
    loader.style.display = "flex";

    let data = {};
    let elements = form.elements;

    for (let i = 0; i < elements.length; i++) {
        let element = elements[i];
        if (element.tagName === "INPUT" || element.tagName === "SELECT") {
            data[element.name] = element.value;
        }
    }
    fetch("/api/predict/wheat-type", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
    })
        .then((response) => response.json())
        .then((data) => {
            console.log("Prediction successful", data);
            result.innerHTML = "Wheat Type: " + data.prediction;
            form.querySelector("input[type=submit]").disabled = false;
            loader.style.display = "none";
        })
        .catch((error) => {
            console.error("Error:", error);
            alert("Error occurred. Please try again.");
            form.querySelector("input[type=submit]").disabled = false;
            loader.style.display = "none";
        });
});

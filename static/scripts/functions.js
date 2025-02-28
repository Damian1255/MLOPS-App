function highlightElement(element, color) {
    element.style.borderColor = color;
}

function create_fields(data, form, ignore_list, custom_label) {
    let outer_div = document.createElement("div");
    outer_div.setAttribute("class", "form-group");

    for (let key in data.attributes) {
        if (ignore_list.includes(key)) {
            continue;
        }

        // div for each attribute
        let div = document.createElement("div");

        // label for each attribute
        let label = document.createElement("label");
        label.setAttribute("for", key);
        label.innerHTML = custom_label[key] ? custom_label[key] : removeUndersore(key);
        div.appendChild(label);

        if (data.attributes[key].type === "object") {
            let select = document.createElement("select");
            let option = document.createElement("option");

            select.setAttribute("id", key);
            select.setAttribute("name", key);
            option.setAttribute("value", "");
            option.innerHTML = "Select " + removeUndersore(key);
            select.appendChild(option);

            // sort the unique values
            data.attributes[key].unique.sort();

            for (let i = 0; i < data.attributes[key].unique.length; i++) {
                let option = document.createElement("option");
                option.setAttribute("value", data.attributes[key].unique[i]);
                option.innerHTML = data.attributes[key].unique[i];
                select.appendChild(option);
            }

            div.appendChild(select);
            outer_div.appendChild(div);
        } else if (
            data.attributes[key].type === "float64" ||
            data.attributes[key].type === "float32"
        ) {
            let input = document.createElement("input");
            input.setAttribute("type", "number");
            input.setAttribute("id", key);
            input.setAttribute("name", key);
            input.setAttribute("min", data.attributes[key].min);
            input.setAttribute("max", data.attributes[key].max);
            input.setAttribute("placeholder", key);

            div.appendChild(input);
            outer_div.appendChild(div);
        } else if (data.attributes[key].type === "int64" || data.attributes[key].type === "int32") {
            // slider for integer values
            // p to display the value of the slider
            let p = document.createElement("p");
            p.setAttribute("id", key + "_value");
            p.innerHTML = data.attributes[key].min;
            div.appendChild(p);

            let input = document.createElement("input");
            input.setAttribute("type", "range");
            input.setAttribute("id", key);
            input.setAttribute("name", key);
            input.setAttribute("min", data.attributes[key].min);
            input.setAttribute("max", data.attributes[key].max);
            input.setAttribute("value", data.attributes[key].min);

            // event listener to update the value of the slider
            input.addEventListener("input", function () {
                p.innerHTML = input.value;
            });

            div.appendChild(input);
            outer_div.appendChild(div);
        } else if (data.attributes[key].type === "string") {
            let input = document.createElement("input");
            input.setAttribute("type", "text");
            input.setAttribute("id", key);
            input.setAttribute("name", key);
            input.setAttribute("placeholder", key);

            div.appendChild(input);
            outer_div.appendChild(div);
        }
    }
    form.appendChild(outer_div);
    // error message
    let p = document.createElement("p");
    p.setAttribute("id", "error");
    p.style.color = "red";
    form.appendChild(p);

    let submit = document.createElement("input");
    submit.setAttribute("type", "submit");
    form.appendChild(submit);
}

function removeUndersore(text) {
    return text.replace(/_/g, " ");
}

function validateForm(form) {
    document.getElementById("error").innerHTML = "";
    let elements = form.elements;
    valid = true;

    for (let i = 0; i < elements.length; i++) {
        let element = elements[i];
        if (element.tagName === "INPUT" || element.tagName === "SELECT") {
            // if button ignore
            if (element.type === "submit") {
                continue;
            }

            if (element.value === "") {
                highlightElement(element, "red");
                valid = false;
            } else {
                highlightElement(element, "#e0e0e0");
            }
        }
    }
    if (valid === false) {
        document.getElementById("error").innerHTML = "Please fill all the fields.";
    }

    return valid;
}

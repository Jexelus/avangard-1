function GetResult() {
    var c1 = document.getElementById("control_01");
    var c2 = document.getElementById("control_02");
    var f0 = document.getElementById("control_03");
    var f1 = document.getElementById("control_04");
    var f3 = document.getElementById("control_05");
    var t50 = document.getElementById("control_06");
    var t100 = document.getElementById("control_07");
    var t300 = document.getElementById("control_08");
    var t500 = document.getElementById("control_09");
    var ac2 = document.getElementById("actions_2");
    var price = document.getElementById("price");
    var ac2_1 = document.getElementById("actions_2_c1");
    var ac2_2 = document.getElementById("actions_2_c2");
    var ac2_3 = document.getElementById("actions_2_c3");

    if (c1.checked) {
        ac2_1.setAttribute('style', 'display:block;');
        ac2_3.setAttribute('style', 'display:block;');
        ac2.setAttribute('style', 'display:flex;');
        if (f0.checked) {
            if (t50.checked) {
                price.innerText = "от 13400р"
            }
            if (t100.checked) {
                price.innerText = "от 21000р"
            }
            if (t300.checked) {
                price.innerText = "от 57900р"
            }
            if (t500.checked) {
                price.innerText = "от 80000р"
            }
        }
        if (f1.checked) {
            if (t50.checked) {
                price.innerText = "от 13650р"
            }
            if (t100.checked) {
                price.innerText = "от 23500р"
            }
            if (t300.checked) {
                price.innerText = "от 59400р"
            }
            if (t500.checked) {
                price.innerText = "от 82500р"
            }
        }
        if (f3.checked) {
            if (t50.checked) {
                price.innerText = "от 14650р"
            }
            if (t100.checked) {
                price.innerText = "от 25500р"
            }
            if (t300.checked) {
                price.innerText = "от 65400р"
            }
            if (t500.checked) {
                price.innerText = "от 92500р"
            }
        }
    }
    if (c2.checked) {
        ac2_1.setAttribute('style', 'display:none;');
        ac2_3.setAttribute('style', 'display:none;');
        f1.checked = true;
        if (t50.checked) {
            price.innerText = "от 7200р"
        }
        if (t100.checked) {
            price.innerText = "от 12400р"
        }
        if (t300.checked) {
            price.innerText = "от 36225р"
        }
        if (t500.checked) {
            price.innerText = "от 56250р"
        }
    }
}
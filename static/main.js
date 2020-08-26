// These are never reassigned so we use const
const amount = document.querySelector("#amount");
const currencyCode = document.querySelector("#currency");
const priceShowcase = document.querySelector("#price-showcase");

// formatter may change later, so we use let
let formatter = new Intl.NumberFormat("de-DE", {
    style: "currency",
    currency: "EUR"
});

amount.addEventListener("input", updatePrice);

currencyCode.addEventListener("change", function () {
    switch (currencyCode.value) {
        case "978":
            return changeFormat("de-DE", "EUR");
        case "840":
            return changeFormat("en-US", "USD");
        case "949":
            return changeFormat("tr-TR", "TRY");
        default:
            return;
    }
});

function changeFormat(locale, currency) {
    formatter = new Intl.NumberFormat(locale, {
        style: "currency",
        currency
    });
    updatePrice();
}

function updatePrice() {
    priceShowcase.textContent = formatter.format(amount.value / 100);
}
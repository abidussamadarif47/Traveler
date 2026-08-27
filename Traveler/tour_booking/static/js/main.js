document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("bookingForm");
    const persons = document.getElementById("totalPersons");
    const total = document.getElementById("bookingTotal");
    if (form && persons && total) {
        const price = Number(form.dataset.price || 0);
        const update = () => {
            const qty = Math.max(Number(persons.value || 1), 1);
            total.textContent = `৳${(price * qty).toFixed(2)}`;
        };
        persons.addEventListener("input", update);
        update();
    }
});

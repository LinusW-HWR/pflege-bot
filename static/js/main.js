document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('openModalBtn').addEventListener('click', openModalButtonListener);
    document.getElementById('confirmBtn').addEventListener('click', confirmCreateRequestButtonListener);

    var typeInput = document.getElementById("typeInput");
    typeInput.addEventListener("change", function() {
        var medicineInput = document.getElementById("medicineInput");
        requestTypeChangeListener(typeInput, medicineInput);
    });

    document.getElementById('yesButton').addEventListener('click', sendHomeYesButtonListener);

    var medicineInput = document.getElementById('medicineInput');
    medicineInput.disabled = true;

    registerSocketEvents();
    reloadRequests();
    headlineAnimation();
});

function headlineAnimation() {
    var typed = new Typed('#element', {
        strings: ['Lieferung', 'Abholung', 'Pflege.'],
        typeSpeed: 100,
        backSpeed: 150,
        backDelay: 700,
        startDelay: 800
    });
}

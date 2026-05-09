function toggleModal() {
    document.getElementById('modal').classList.toggle('hidden');
}

function openModal(btn) {
    const id = btn.dataset.id;
    const gender = btn.dataset.gender;

    document.querySelector('#modal form').action = `/gender/update/${id}/`;
    document.querySelector('#modal input[name="gender"]').value = gender;
    document.querySelector('#modal h3').textContent = `Update Gender: ${gender}`;

    toggleModal();
}

function toggleDeleteModal() {
    document.getElementById('delete-modal').classList.toggle('hidden');
}

function openDeleteModal(btn) {
    const id = btn.dataset.id;
    const gender = btn.dataset.gender;

    document.querySelector('#delete-modal form').action = `/gender/delete/${id}/`;
    document.querySelector('#delete-modal h3').textContent = `Delete Gender: ${gender}?`;

    toggleDeleteModal();
}


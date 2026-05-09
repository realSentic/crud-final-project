function toggleUserModal() {
    document.getElementById('user-modal').classList.toggle('hidden');
}

function openUserModal(btn) {
    const id = btn.dataset.id;
    const full_name = btn.dataset.full_name;
    const gender = btn.dataset.gender;
    const birth_date = btn.dataset.birth_date;
    const address = btn.dataset.address;
    const contact_number = btn.dataset.contact_number;
    const email = btn.dataset.email;
    const username = btn.dataset.username;
    const profile_picture = btn.dataset.profile_picture;

    document.querySelector('#user-modal form').action = `/user/update/${id}/`;
    document.querySelector('#user-modal h3').textContent = `Update User: ${full_name}`;
    document.querySelector('#user-modal input[name="full_name"]').value = full_name;
    document.querySelector('#user-modal select[name="gender"]').value = gender;
    document.querySelector('#user-modal input[name="birth_date"]').value = birth_date;
    document.querySelector('#user-modal input[name="address"]').value = address;
    document.querySelector('#user-modal input[name="contact_number"]').value = contact_number;
    document.querySelector('#user-modal input[name="email"]').value = email;
    document.querySelector('#user-modal input[name="username"]').value = username;

    const pic = document.getElementById('current-profile-pic');

    if (profile_picture) {
        pic.src = `/media/${profile_picture}`;
        pic.style.display = 'block';
    } else {
        pic.style.display = 'none';
    }

    const fileName = profile_picture ? profile_picture.split('/').pop() : 'none';

    toggleUserModal();
}

function toggleUserDeleteModal() {
    document.getElementById('user-delete-modal').classList.toggle('hidden');
}

function openUserDeleteModal(btn) {
    const id = btn.dataset.id;
    const full_name = btn.dataset.full_name;
    const profile_picture = btn.dataset.profile_picture;

    document.querySelector('#user-delete-modal form').action = `/user/delete/${id}/`;
    document.querySelector('#user-delete-modal h3').textContent = `Delete User: ${full_name}?`;

    const deletePic = document.getElementById('delete-user-pic');
    
    if (profile_picture && profile_picture !== "None" && profile_picture.trim() !== "") {
        deletePic.src = `/media/${profile_picture}`;
        deletePic.style.display = 'block';
    } else {
        deletePic.style.display = 'none';
        deletePic.src = ''; 
    }

    toggleUserDeleteModal();
}

function removeProfilePicture() {
    document.getElementById('remove_profile_picture').value = '1';
    document.getElementById('current-profile-pic').src = '';
    document.getElementById('current-profile-pic').style.display = 'none';
    document.getElementById('profile_picture').value = '';
    

    showToast('Profile picture will be removed on save.');
}

function showToast(message) {
    const container = document.querySelector('.fixed.bottom-5.right-5');
    const toast = document.createElement('div');
    toast.className = 'motion-preset-slide-up bg-yellow-600 text-white text-base font-semibold px-6 py-4 rounded-xl shadow-2xl flex items-center gap-3 min-w-[320px]';
    toast.innerHTML = `<span>${message}</span>`;
    container.appendChild(toast);

    setTimeout(() => {
        toast.classList.add('motion-opacity-out-0');
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}
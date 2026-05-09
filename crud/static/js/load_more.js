const btn = document.getElementById('load-more-btn');

if (btn) {
    btn.addEventListener('click', async () => {
        const nextPage = btn.dataset.nextPage;

        const response = await fetch(`?page=${nextPage}`);
        const html = await response.text();

        const parser = new DOMParser();
        const doc = parser.parseFromString(html, 'text/html');
        const newRows = doc.querySelectorAll('#user-table-body tr');
        const newBtn = doc.getElementById('load-more-btn');

        newRows.forEach(row => document.getElementById('user-table-body').appendChild(row));

        if (newBtn) {
            btn.dataset.nextPage = newBtn.dataset.nextPage;
        } else {
            document.getElementById('load-more-container').remove();
        }
    });
}
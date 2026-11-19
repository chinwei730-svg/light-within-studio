// 相簿放大瀏覽：點 .album-item 開啟，支援左右切換、Esc 關閉、鍵盤方向鍵、手機左右滑動
document.addEventListener('DOMContentLoaded', function () {
    var items = Array.prototype.slice.call(document.querySelectorAll('.album-item'));
    if (!items.length) { return; }

    var box = document.createElement('div');
    box.className = 'lightbox';
    box.setAttribute('role', 'dialog');
    box.setAttribute('aria-modal', 'true');
    box.setAttribute('aria-label', '照片放大瀏覽');
    box.innerHTML =
        '<button type="button" class="lightbox-close" aria-label="關閉">&times;</button>' +
        '<button type="button" class="lightbox-prev" aria-label="上一張">&#8249;</button>' +
        '<img alt="">' +
        '<button type="button" class="lightbox-next" aria-label="下一張">&#8250;</button>' +
        '<div class="lightbox-count"></div>';
    document.body.appendChild(box);

    var img = box.querySelector('img');
    var count = box.querySelector('.lightbox-count');
    var current = 0;

    function show(i) {
        current = (i + items.length) % items.length;
        var link = items[current];
        img.src = link.getAttribute('href');
        img.alt = link.querySelector('img').alt;
        count.textContent = (current + 1) + ' / ' + items.length;
    }

    function open(i) {
        show(i);
        box.classList.add('is-open');
        document.body.style.overflow = 'hidden';
    }

    function close() {
        box.classList.remove('is-open');
        document.body.style.overflow = '';
        img.removeAttribute('src');
    }

    items.forEach(function (link, i) {
        link.addEventListener('click', function (e) {
            e.preventDefault();
            open(i);
        });
    });

    box.querySelector('.lightbox-close').addEventListener('click', close);
    box.querySelector('.lightbox-prev').addEventListener('click', function () { show(current - 1); });
    box.querySelector('.lightbox-next').addEventListener('click', function () { show(current + 1); });
    box.addEventListener('click', function (e) { if (e.target === box) { close(); } });

    document.addEventListener('keydown', function (e) {
        if (!box.classList.contains('is-open')) { return; }
        if (e.key === 'Escape') { close(); }
        else if (e.key === 'ArrowLeft') { show(current - 1); }
        else if (e.key === 'ArrowRight') { show(current + 1); }
    });

    var startX = null;
    box.addEventListener('touchstart', function (e) { startX = e.touches[0].clientX; }, { passive: true });
    box.addEventListener('touchend', function (e) {
        if (startX === null) { return; }
        var dx = e.changedTouches[0].clientX - startX;
        startX = null;
        if (Math.abs(dx) > 50) { show(current + (dx < 0 ? 1 : -1)); }
    }, { passive: true });
});

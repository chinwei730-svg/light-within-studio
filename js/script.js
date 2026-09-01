// 等待頁面載入完成
document.addEventListener('DOMContentLoaded', function() {

    // 手機版選單切換
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.nav-menu');

    if (hamburger && navMenu) {
        hamburger.addEventListener('click', function() {
            navMenu.classList.toggle('active');

            // 漢堡選單動畫
            this.classList.toggle('active');
        });
    }

    // 點擊選單項目後關閉選單
    // 綁 .nav-menu 底下所有 <a>，不是只綁 .nav-link：
    // 領域下拉裡的子項目沒有 .nav-link 這個 class，
    // 只綁 .nav-link 的話點子項目選單不會收起來。
    const navLinks = navMenu ? navMenu.querySelectorAll('a') : [];
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            if (navMenu) { navMenu.classList.remove('active'); }
            if (hamburger) { hamburger.classList.remove('active'); }
        });
    });

    // 平滑滾動
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');

            // 只攔截本頁錨點（#開頭）。子頁面的 index.html#courses 這類跨頁連結
            // 必須讓瀏覽器正常導頁，否則會被 preventDefault 擋成死連結。
            if (!targetId || targetId.charAt(0) !== '#') {
                return;
            }

            const targetSection = document.querySelector(targetId);
            if (!targetSection) {
                return;
            }

            e.preventDefault();
            const offsetTop = targetSection.offsetTop - 60;
            window.scrollTo({
                top: offsetTop,
                behavior: 'smooth'
            });
        });
    });

    // 滾動時改變導航列樣式
    window.addEventListener('scroll', function() {
        const navbar = document.querySelector('.navbar');
        if (window.scrollY > 100) {
            navbar.style.background = 'rgba(255, 255, 255, 0.98)';
        } else {
            navbar.style.background = '#fff';
        }
    });

    // 表單提交處理
    const contactForm = document.querySelector('.contact-form form');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();

            // 這裡可以加入表單驗證和提交邏輯
            // 目前只顯示確認訊息
            alert('感謝您的留言！我們會盡快回覆您。');

            // 清空表單
            this.reset();
        });
    }

    // 圖片懶加載效果（當您加入真實圖片後可以使用）
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // 觀察所有卡片元素
    const cards = document.querySelectorAll('.course-card, .gallery-item');
    cards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.6s, transform 0.6s';
        observer.observe(card);
    });
});

// ============================================================
// 未來擴展版：領域頁的課程篩選
// ------------------------------------------------------------
// 同一個領域超過四、五門課之後，訪客需要的是分類而不是捲動。
// 這裡只做 class 的加減，沒有課程資料庫也能用；
// 頁面上沒有 .course-filter 時整段不會執行。
// 要退回純奧剛版時，把這一整段刪掉即可。
// ============================================================
document.addEventListener('DOMContentLoaded', function() {
    var groups = document.querySelectorAll('.course-filter');

    groups.forEach(function(group) {
        // 篩選列後面第一個課程格，就是這組按鈕要控制的對象
        var grid = group.parentElement.querySelector('.course-grid');
        if (!grid) {
            return;
        }

        var buttons = group.querySelectorAll('.filter-btn');
        var cards = grid.querySelectorAll('.course-card');

        buttons.forEach(function(button) {
            button.addEventListener('click', function() {
                var wanted = this.getAttribute('data-filter');

                buttons.forEach(function(b) {
                    b.classList.remove('is-active');
                });
                this.classList.add('is-active');

                cards.forEach(function(card) {
                    var level = card.getAttribute('data-level');
                    var show = (wanted === 'all' || level === wanted);
                    card.classList.toggle('is-hidden', !show);
                });
            });
        });
    });
});

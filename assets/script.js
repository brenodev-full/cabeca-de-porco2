/* =============================================================
   CABEÇA DE PORCO — Main Script
   Premium animations + full interactivity (no framework needed)
   ============================================================= */

document.addEventListener('DOMContentLoaded', () => {

    /* ----------------------------------------------------------
       1. NAV — scroll-aware shrink + active link highlight
    ---------------------------------------------------------- */
    const nav = document.querySelector('.nav');

    const updateNav = () => {
        if (window.scrollY > 60) {
            nav.classList.add('scrolled');
        } else {
            nav.classList.remove('scrolled');
        }
    };
    window.addEventListener('scroll', updateNav, { passive: true });
    updateNav();

    /* Highlight active nav link based on scroll position */
    const sections = document.querySelectorAll('section[id]');
    const navAnchors = document.querySelectorAll('.nav-links a[href^="#"]');

    const highlightNav = () => {
        let current = '';
        sections.forEach(sec => {
            if (window.scrollY >= sec.offsetTop - 140) current = sec.id;
        });
        navAnchors.forEach(a => {
            a.classList.toggle('active-link', a.getAttribute('href') === `#${current}`);
        });
    };
    window.addEventListener('scroll', highlightNav, { passive: true });


    /* ----------------------------------------------------------
       2. MOBILE MENU
    ---------------------------------------------------------- */
    const burger = document.querySelector('.burger');
    const navLinks = document.querySelector('.nav-links');

    if (burger && navLinks) {
        burger.addEventListener('click', () => {
            burger.classList.toggle('open');
            navLinks.classList.toggle('mobile-open');
        });

        navLinks.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                burger.classList.remove('open');
                navLinks.classList.remove('mobile-open');
            });
        });
    }


    /* ----------------------------------------------------------
       3. SCROLL REVEAL — IntersectionObserver (replaces forced CSS)
    ---------------------------------------------------------- */
    const revealEls = document.querySelectorAll('.reveal');

    const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                // Respect any existing transition-delay set inline
                entry.target.classList.add('in');
                revealObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1, rootMargin: '0px 0px -60px 0px' });

    revealEls.forEach(el => revealObserver.observe(el));


    /* ----------------------------------------------------------
       4. HERO PARALLAX (subtle, 60fps-safe with RAF)
    ---------------------------------------------------------- */
    const heroBg = document.querySelector('.hero-bg');
    let ticking = false;

    if (heroBg) {
        window.addEventListener('scroll', () => {
            if (!ticking) {
                requestAnimationFrame(() => {
                    const scrolled = window.scrollY;
                    if (scrolled < window.innerHeight) {
                        heroBg.style.transform = `scale(1.05) translateY(${scrolled * 0.25}px)`;
                    }
                    ticking = false;
                });
                ticking = true;
            }
        }, { passive: true });
    }


    /* ----------------------------------------------------------
       5. FEATURE CARDS — magnetic hover effect
    ---------------------------------------------------------- */
    document.querySelectorAll('.feature-card').forEach(card => {
        card.addEventListener('mousemove', e => {
            const rect = card.getBoundingClientRect();
            const x = ((e.clientX - rect.left) / rect.width) * 100;
            const y = ((e.clientY - rect.top) / rect.height) * 100;
            card.style.setProperty('--mx', `${x}%`);
            card.style.setProperty('--my', `${y}%`);
        });
    });


    /* ----------------------------------------------------------
       6. MENU TABS — smooth fade-slide transition
    ---------------------------------------------------------- */
    const tabs = document.querySelectorAll('.tabs .tab');
    const menuItems = document.querySelectorAll('.menu-item');
    const menuGrid = document.querySelector('.menu-grid');

    if (tabs.length > 0) {
        tabs.forEach(tab => {
            tab.addEventListener('click', () => {
                if (tab.classList.contains('active')) return;

                tabs.forEach(t => t.classList.remove('active'));
                tab.classList.add('active');

                const targetCategory = tab.getAttribute('data-target');

                // Phase 1: fade current items out together
                const visibleItems = [...menuItems].filter(i => i.style.display !== 'none');

                if (visibleItems.length === 0) {
                    showNewItems(targetCategory);
                    return;
                }

                visibleItems.forEach(item => {
                    item.style.transition = 'opacity 0.22s ease, transform 0.22s ease';
                    item.style.opacity = '0';
                    item.style.transform = 'translateY(-8px)';
                });

                // Phase 2: after fade-out, hide old and reveal new
                setTimeout(() => {
                    visibleItems.forEach(item => { item.style.display = 'none'; });
                    showNewItems(targetCategory);
                }, 240);
            });
        });
    }

    function showNewItems(category) {
        const targets = [...menuItems].filter(i => i.getAttribute('data-category') === category);

        targets.forEach((item, idx) => {
            item.style.display = 'flex';
            item.style.opacity = '0';
            item.style.transform = 'translateY(18px)';
            item.style.transition = 'none';
        });

        // Stagger fade-in
        targets.forEach((item, idx) => {
            requestAnimationFrame(() => {
                setTimeout(() => {
                    item.style.transition = `opacity 0.38s ease ${idx * 45}ms, transform 0.38s cubic-bezier(0.22, 1, 0.36, 1) ${idx * 45}ms`;
                    item.style.opacity = '1';
                    item.style.transform = 'translateY(0)';
                }, 10);
            });
        });
    }


    /* ----------------------------------------------------------
       7. REVIEWS CAROUSEL — auto-play + swipe support
    ---------------------------------------------------------- */
    const reviewTrack = document.querySelector('.reviews-track');
    const dots = document.querySelectorAll('.review-dots button');
    let currentSlide = 0;
    let autoPlayTimer;

    function goToSlide(index) {
        currentSlide = index;
        reviewTrack.style.transform = `translateX(-${index * 100}%)`;
        dots.forEach((d, i) => d.classList.toggle('active', i === index));
    }

    if (reviewTrack && dots.length > 0) {
        dots.forEach((dot, index) => {
            dot.addEventListener('click', () => {
                clearInterval(autoPlayTimer);
                goToSlide(index);
                startAutoPlay();
            });
        });

        // Auto-play every 5s
        function startAutoPlay() {
            autoPlayTimer = setInterval(() => {
                goToSlide((currentSlide + 1) % dots.length);
            }, 5000);
        }
        startAutoPlay();

        // Touch/swipe support
        let touchStartX = 0;
        reviewTrack.addEventListener('touchstart', e => { touchStartX = e.touches[0].clientX; }, { passive: true });
        reviewTrack.addEventListener('touchend', e => {
            const delta = touchStartX - e.changedTouches[0].clientX;
            if (Math.abs(delta) > 50) {
                clearInterval(autoPlayTimer);
                if (delta > 0) goToSlide(Math.min(currentSlide + 1, dots.length - 1));
                else goToSlide(Math.max(currentSlide - 1, 0));
                startAutoPlay();
            }
        });
    }


    /* ----------------------------------------------------------
       8. STAT NUMBERS — count-up animation
    ---------------------------------------------------------- */
    const statNums = document.querySelectorAll('.stat .num');

    const countObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (!entry.isIntersecting) return;

            const el = entry.target;
            const raw = el.textContent.trim(); // e.g. "12h", "+50", "24/7"
            const numMatch = raw.match(/\d+/);
            if (!numMatch) return;

            const end = parseInt(numMatch[0]);
            const prefix = raw.startsWith('+') ? '+' : '';
            const suffix = raw.replace(/[+\d]/g, '');
            let start = 0;
            const duration = 1400;
            const startTime = performance.now();

            const tick = (now) => {
                const progress = Math.min((now - startTime) / duration, 1);
                const eased = 1 - Math.pow(1 - progress, 3); // ease-out cubic
                const val = Math.round(start + (end - start) * eased);
                el.textContent = `${prefix}${val}${suffix}`;
                if (progress < 1) requestAnimationFrame(tick);
            };
            requestAnimationFrame(tick);
            countObserver.unobserve(el);
        });
    }, { threshold: 0.5 });

    statNums.forEach(el => countObserver.observe(el));


    /* ----------------------------------------------------------
       9. CART LOGIC
    ---------------------------------------------------------- */
    const cartBtn = document.querySelector('.cart-btn');
    const cartClose = document.querySelector('.cart-close');
    const cartDrawer = document.querySelector('.cart-drawer');
    const cartOverlay = document.querySelector('.cart-overlay');
    const toast = document.querySelector('.toast');
    const WHATSAPP_NUMBER = '552124129370';

    let cart = [];

    function toggleCart() {
        if (!cartDrawer || !cartOverlay) return;
        const isOpen = cartDrawer.classList.toggle('open');
        cartOverlay.classList.toggle('open');
        cartDrawer.setAttribute('aria-hidden', !isOpen);
    }

    if (cartBtn) cartBtn.addEventListener('click', toggleCart);
    if (cartClose) cartClose.addEventListener('click', toggleCart);
    if (cartOverlay) cartOverlay.addEventListener('click', toggleCart);

    function updateCartUI() {
        const cartBody = document.querySelector('.cart-body');
        const cartEmpty = document.querySelector('.cart-empty');
        const cartTotalCount = document.querySelector('.cart-total span:first-child');
        const cartTotalPrice = document.querySelector('.cart-total span:last-child');
        const checkoutBtn = document.querySelector('.cart-foot .btn-primary');
        const cartCount = document.querySelector('.cart-count');

        if (!cartBody) return;

        let totalItems = 0;
        let totalPrice = 0;
        cart.forEach(item => {
            totalItems += item.quantity;
            totalPrice += item.price * item.quantity;
        });

        if (cartTotalCount) cartTotalCount.textContent = `Total (${totalItems} item${totalItems !== 1 ? 's' : ''})`;
        if (cartTotalPrice) cartTotalPrice.textContent = `R$ ${totalPrice.toFixed(2).replace('.', ',')}`;

        // Cart count badge on button
        if (cartCount) {
            cartCount.textContent = totalItems;
            cartCount.style.display = totalItems > 0 ? 'grid' : 'none';
        }

        // Clear rendered lines
        cartBody.querySelectorAll('.cart-line').forEach(el => el.remove());

        if (cart.length === 0) {
            if (cartEmpty) cartEmpty.style.display = 'block';
            if (checkoutBtn) {
                checkoutBtn.style.opacity = '0.5';
                checkoutBtn.style.pointerEvents = 'none';
                checkoutBtn.removeAttribute('href');
            }
        } else {
            if (cartEmpty) cartEmpty.style.display = 'none';
            if (checkoutBtn) {
                checkoutBtn.style.opacity = '1';
                checkoutBtn.style.pointerEvents = 'auto';
            }

            cart.forEach((item, idx) => {
                cartBody.insertAdjacentHTML('beforeend', `
                    <div class="cart-line">
                        <div style="flex:1">
                            <div class="name">${item.name}</div>
                            <div class="qty">R$ ${item.price.toFixed(2).replace('.', ',')}</div>
                        </div>
                        <div class="actions">
                            <button onclick="updateCartItemQuantity(${idx}, -1)">-</button>
                            <span style="color:#f3ead8;font-size:14px;min-width:18px;text-align:center">${item.quantity}</span>
                            <button onclick="updateCartItemQuantity(${idx}, 1)">+</button>
                        </div>
                    </div>
                `);
            });

            if (checkoutBtn) {
                let waText = 'Olá! Gostaria de fazer o seguinte pedido:%0A%0A';
                cart.forEach(item => {
                    waText += `${item.quantity}x ${item.name} - R$ ${(item.price * item.quantity).toFixed(2).replace('.', ',')}%0A`;
                });
                waText += `%0ATotal: R$ ${totalPrice.toFixed(2).replace('.', ',')}`;
                checkoutBtn.setAttribute('href', `https://wa.me/${WHATSAPP_NUMBER}?text=${waText}`);
            }
        }
    }

    window.updateCartItemQuantity = function(index, delta) {
        if (!cart[index]) return;
        cart[index].quantity += delta;
        if (cart[index].quantity <= 0) cart.splice(index, 1);
        updateCartUI();
    };

    // Add to cart buttons — delegate to handle dynamically shown items
    document.querySelector('.menu-grid')?.addEventListener('click', e => {
        const btn = e.target.closest('.add-btn');
        if (!btn || btn.textContent.trim() === 'Consultar') return;

        const article = btn.closest('.menu-item');
        if (!article) return;

        const name = article.querySelector('h4').textContent.trim();
        const priceStr = article.querySelector('.menu-price').textContent;
        const price = parseFloat(priceStr.replace('R$', '').replace(',', '.').trim()) || 0;

        const existing = cart.find(i => i.name === name);
        if (existing) existing.quantity++;
        else cart.push({ name, price, quantity: 1 });

        updateCartUI();

        // Pulse the add button
        btn.classList.add('added');
        setTimeout(() => btn.classList.remove('added'), 600);

        // Toast
        if (toast) {
            const toastSpan = toast.querySelector('.ok');
            if (toastSpan) toast.querySelector('.ok').insertAdjacentText('afterend', ` ${name.split(' ').slice(0, 2).join(' ')} adicionado!`);
            toast.classList.add('show');
            setTimeout(() => {
                toast.classList.remove('show');
                // Clear the extra text for next time
                toast.innerHTML = '<span class="ok">✓</span>';
            }, 2200);
        }
    });

    updateCartUI();


    /* ----------------------------------------------------------
       10. SMOOTH ANCHOR SCROLL with offset for fixed nav
    ---------------------------------------------------------- */
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', e => {
            const target = document.querySelector(anchor.getAttribute('href'));
            if (!target) return;
            e.preventDefault();
            const top = target.getBoundingClientRect().top + window.scrollY - 80;
            window.scrollTo({ top, behavior: 'smooth' });
        });
    });


    /* ----------------------------------------------------------
       11. PAGE ENTRANCE — stagger hero elements on load
    ---------------------------------------------------------- */
    const heroContent = document.querySelector('.hero-content');
    if (heroContent) {
        const children = heroContent.querySelectorAll(':scope > *');
        children.forEach((el, i) => {
            el.style.opacity = '0';
            el.style.transform = 'translateY(28px)';
            el.style.transition = `opacity 0.7s ease ${i * 120 + 200}ms, transform 0.7s cubic-bezier(0.22, 1, 0.36, 1) ${i * 120 + 200}ms`;
            requestAnimationFrame(() => {
                el.style.opacity = '1';
                el.style.transform = 'translateY(0)';
            });
        });
    }

});

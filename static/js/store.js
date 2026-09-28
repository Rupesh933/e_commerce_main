function copyPromoCode(code) {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(code).then(function() {
            var icon = document.getElementById('copyIcon');
            var badge = document.getElementById('couponBadge');
            if (icon) icon.className = 'fa fa-check text-success';
            if (badge) badge.style.borderColor = '#2ecc71';
            setTimeout(function() {
                if (icon) icon.className = 'fa fa-copy';
                if (badge) badge.style.borderColor = '#ffd700';
            }, 2000);
        });
    }
}

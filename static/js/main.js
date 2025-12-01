// Main JavaScript for News Aggregator

$(document).ready(function() {
    // Save Article Functionality
    $('.save-article-btn').on('click', function() {
        const btn = $(this);
        const newsId = btn.data('news-id');
        const isSaved = btn.data('saved') === true;
        const csrftoken = getCookie('csrftoken');
        
        if (isSaved) {
            // Unsave article
            $.ajax({
                url: `/unsave-article/${newsId}/`,
                type: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken
                },
                success: function(response) {
                    if (response.status === 'unsaved') {
                        btn.removeClass('btn-warning').addClass('btn-outline-secondary');
                        btn.find('i').removeClass('bi-bookmark-fill').addClass('bi-bookmark');
                        btn.data('saved', false);
                        showToast('Article removed from saved list!', 'info');
                    }
                },
                error: function() {
                    showToast('Error removing article. Please try again.', 'danger');
                }
            });
        } else {
            // Save article
            $.ajax({
                url: `/save-article/${newsId}/`,
                type: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken
                },
                success: function(response) {
                    if (response.status === 'saved' || response.status === 'already_saved') {
                        btn.removeClass('btn-outline-secondary').addClass('btn-warning');
                        btn.find('i').removeClass('bi-bookmark').addClass('bi-bookmark-fill');
                        btn.data('saved', true);
                        showToast(response.message, 'success');
                    }
                },
                error: function() {
                    showToast('Error saving article. Please try again.', 'danger');
                }
            });
        }
    });
    
    // Unsave Article from Dashboard
    $('.unsave-article-btn').on('click', function() {
        const btn = $(this);
        const newsId = btn.data('news-id');
        const card = btn.closest('.col-md-6, .col-lg-4');
        const csrftoken = getCookie('csrftoken');
        
        if (confirm('Are you sure you want to remove this article from your saved list?')) {
            $.ajax({
                url: `/unsave-article/${newsId}/`,
                type: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken
                },
                success: function(response) {
                    if (response.status === 'unsaved') {
                        card.fadeOut(300, function() {
                            $(this).remove();
                            // Check if no more articles
                            if ($('.col-md-6, .col-lg-4').length === 0) {
                                location.reload();
                            }
                        });
                        showToast('Article removed from saved list!', 'success');
                    }
                },
                error: function() {
                    showToast('Error removing article. Please try again.', 'danger');
                }
            });
        }
    });
    
    // Auto-dismiss alerts after 5 seconds
    setTimeout(function() {
        $('.alert').fadeOut('slow');
    }, 5000);
});

// Get CSRF Token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Show Toast Notification
function showToast(message, type = 'info') {
    const toast = $(`
        <div class="toast align-items-center text-white bg-${type} border-0" role="alert" aria-live="assertive" aria-atomic="true" style="position: fixed; top: 20px; right: 20px; z-index: 9999;">
            <div class="d-flex">
                <div class="toast-body">${message}</div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        </div>
    `);
    
    $('body').append(toast);
    const bsToast = new bootstrap.Toast(toast[0]);
    bsToast.show();
    
    toast.on('hidden.bs.toast', function() {
        $(this).remove();
    });
}


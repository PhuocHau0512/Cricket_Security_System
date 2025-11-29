// Custom JavaScript for Cricket Security System

// Global functions
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('vi-VN');
}

function showLoading() {
    // Hiển thị loading indicator
    $('#loadingIndicator').show();
}

function hideLoading() {
    // Ẩn loading indicator
    $('#loadingIndicator').hide();
}

// Risk calculation
function calculateRiskScore(likelihood, impact) {
    const riskMatrix = {
        'rare': {'insignificant': 1, 'minor': 2, 'moderate': 3, 'major': 4, 'catastrophic': 5},
        'unlikely': {'insignificant': 2, 'minor': 4, 'moderate': 6, 'major': 8, 'catastrophic': 10},
        'possible': {'insignificant': 3, 'minor': 6, 'moderate': 9, 'major': 12, 'catastrophic': 15},
        'likely': {'insignificant': 4, 'minor': 8, 'moderate': 12, 'major': 16, 'catastrophic': 20},
        'almost_certain': {'insignificant': 5, 'minor': 10, 'moderate': 15, 'major': 20, 'catastrophic': 25}
    };
    
    return riskMatrix[likelihood][impact];
}

function getRiskLevel(score) {
    if (score <= 4) return { level: 'low', color: 'success' };
    if (score <= 9) return { level: 'medium', color: 'warning' };
    if (score <= 16) return { level: 'high', color: 'danger' };
    return { level: 'extreme', color: 'dark' };
}

// API calls
async function apiCall(endpoint, method = 'GET', data = null) {
    try {
        const options = {
            method: method,
            headers: {
                'Content-Type': 'application/json',
            }
        };
        
        if (data && (method === 'POST' || method === 'PUT')) {
            options.body = JSON.stringify(data);
        }
        
        const response = await fetch(endpoint, options);
        return await response.json();
    } catch (error) {
        console.error('API call failed:', error);
        throw error;
    }
}

// Notification system
function showNotification(message, type = 'info') {
    const alertClass = {
        'success': 'alert-success',
        'error': 'alert-danger',
        'warning': 'alert-warning',
        'info': 'alert-info'
    }[type] || 'alert-info';
    
    const notification = $(`
        <div class="alert ${alertClass} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `);
    
    $('#notifications').append(notification);
    
    // Tự động ẩn sau 5 giây
    setTimeout(() => {
        notification.alert('close');
    }, 5000);
}

// Form validation
function validateRiskForm() {
    const likelihood = $('#likelihood').val();
    const impact = $('#impact').val();
    
    if (!likelihood || !impact) {
        showNotification('Vui lòng chọn cả khả năng xảy ra và mức độ tác động', 'warning');
        return false;
    }
    
    const score = calculateRiskScore(likelihood, impact);
    const riskInfo = getRiskLevel(score);
    
    showNotification(`Điểm rủi ro dự tính: ${score} (${riskInfo.level.toUpperCase()})`, 'info');
    return true;
}

// Initialize when document is ready
$(document).ready(function() {
    // Auto-update risk score when likelihood or impact changes
    $('#likelihood, #impact').on('change', function() {
        const likelihood = $('#likelihood').val();
        const impact = $('#impact').val();
        
        if (likelihood && impact) {
            const score = calculateRiskScore(likelihood, impact);
            const riskInfo = getRiskLevel(score);
            
            $('#riskScorePreview').remove();
            $(this).closest('.mb-3').after(`
                <div id="riskScorePreview" class="alert alert-${riskInfo.color}">
                    <strong>Điểm rủi ro dự tính:</strong> ${score} - Mức độ: ${riskInfo.level.toUpperCase()}
                </div>
            `);
        }
    });
    
    // Auto-hide alerts after 5 seconds
    $('.alert').not('.alert-permanent').delay(5000).fadeOut(300);
    
    // Enable tooltips
    $('[data-bs-toggle="tooltip"]').tooltip();
    
    // Enable popovers
    $('[data-bs-toggle="popover"]').popover();
});

// Export functionality
function exportToCSV(data, filename) {
    const csvContent = "data:text/csv;charset=utf-8," 
        + data.map(row => row.join(",")).join("\n");
    
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", filename);
    document.body.appendChild(link);
    
    link.click();
    document.body.removeChild(link);
}

// Risk matrix visualization
function drawRiskMatrix(risks) {
    // Implementation for interactive risk matrix
    console.log('Drawing risk matrix with data:', risks);
    // This would use Chart.js or D3.js for advanced visualization
}
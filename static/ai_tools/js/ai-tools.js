// ===== AI Tools JavaScript ===== //

// Import base functionality
if (typeof window.TechyVia === 'undefined') {
    window.TechyVia = {};
}

// AI Tools specific functionality
document.addEventListener('DOMContentLoaded', function() {
    console.log('🤖 AI Tools Module Loading...');
    
    // Initialize AI Tools features
    initToolFilters();
    initToolComparison();
    initToolSearch();
    initViewToggle();
    
    console.log('✅ AI Tools Module Loaded');
});

// ===== Tool Filters ===== //
function initToolFilters() {
    const filterLinks = document.querySelectorAll('.filter-list a');
    const complexitySlider = document.getElementById('complexitySlider');
    
    // Handle filter clicks
    filterLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const url = new URL(window.location);
            const href = this.getAttribute('href');
            
            if (href.startsWith('?')) {
                // Parse the query string
                const params = new URLSearchParams(href.substring(1));
                params.forEach((value, key) => {
                    url.searchParams.set(key, value);
                });
            }
            
            // Navigate to filtered results
            window.location.href = url.toString();
        });
    });
    
    // Handle complexity slider
    if (complexitySlider) {
        let timeout;
        complexitySlider.addEventListener('input', function() {
            clearTimeout(timeout);
            timeout = setTimeout(() => {
                const url = new URL(window.location);
                url.searchParams.set('complexity', this.value);
                window.location.href = url.toString();
            }, 500);
        });
    }
}

// ===== Tool Comparison ===== //
function initToolComparison() {
    let compareList = JSON.parse(localStorage.getItem('compareList') || '[]');
    const compareButtons = document.querySelectorAll('.compare-add');
    
    // Update button states based on stored comparison list
    updateCompareButtons();
    
    compareButtons.forEach(button => {
        button.addEventListener('click', function() {
            const toolId = this.dataset.toolId;
            const toolCard = this.closest('.tool-card');
            const toolName = toolCard.querySelector('.tool-title a').textContent;
            
            if (compareList.includes(toolId)) {
                // Remove from compare
                compareList = compareList.filter(id => id !== toolId);
                this.style.background = 'var(--glass-bg)';
                this.style.color = 'var(--text-secondary)';
                showNotification(`${toolName} removed from comparison`, 'info');
            } else {
                // Add to compare
                if (compareList.length >= 4) {
                    showNotification('You can only compare up to 4 tools at once', 'warning');
                    return;
                }
                compareList.push(toolId);
                this.style.background = 'var(--accent)';
                this.style.color = 'white';
                showNotification(`${toolName} added to comparison`, 'success');
            }
            
            // Save to localStorage
            localStorage.setItem('compareList', JSON.stringify(compareList));
            updateCompareFloatingButton();
        });
    });
    
    function updateCompareButtons() {
        compareButtons.forEach(button => {
            const toolId = button.dataset.toolId;
            if (compareList.includes(toolId)) {
                button.style.background = 'var(--accent)';
                button.style.color = 'white';
            }
        });
        updateCompareFloatingButton();
    }
    
    function updateCompareFloatingButton() {
        let floatingButton = document.getElementById('floating-compare');
        
        if (compareList.length >= 2) {
            if (!floatingButton) {
                floatingButton = document.createElement('div');
                floatingButton.id = 'floating-compare';
                floatingButton.innerHTML = `
                    <div class="floating-compare-content">
                        <span class="compare-count">${compareList.length}</span>
                        <span class="compare-text">Tools to Compare</span>
                        <button class="btn-cyber compare-now-btn">
                            <i class="fas fa-balance-scale"></i> Compare Now
                        </button>
                        <button class="btn-outline-cyber clear-compare-btn">
                            <i class="fas fa-times"></i> Clear
                        </button>
                    </div>
                `;
                floatingButton.style.cssText = `
                    position: fixed;
                    bottom: 2rem;
                    left: 50%;
                    transform: translateX(-50%);
                    background: var(--glass-bg);
                    backdrop-filter: blur(20px);
                    border: 1px solid var(--glass-border);
                    border-radius: 15px;
                    padding: 1rem 1.5rem;
                    z-index: 1000;
                    box-shadow: var(--hover-shadow);
                    animation: slideUp 0.3s ease;
                `;
                
                // Add CSS animation
                const style = document.createElement('style');
                style.textContent = `
                    @keyframes slideUp {
                        from { transform: translateX(-50%) translateY(100px); opacity: 0; }
                        to { transform: translateX(-50%) translateY(0); opacity: 1; }
                    }
                    .floating-compare-content {
                        display: flex;
                        align-items: center;
                        gap: 1rem;
                        color: var(--text-primary);
                    }
                    .compare-count {
                        background: var(--primary);
                        color: white;
                        width: 30px;
                        height: 30px;
                        border-radius: 50%;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        font-weight: bold;
                    }
                `;
                document.head.appendChild(style);
                
                document.body.appendChild(floatingButton);
                
                // Add event listeners
                floatingButton.querySelector('.compare-now-btn').addEventListener('click', function() {
                    // Redirect to comparison page with tool IDs
                    const params = new URLSearchParams();
                    compareList.forEach(id => params.append('tools', id));
                    window.location.href = `/ai-tools/compare/?${params.toString()}`;
                });
                
                floatingButton.querySelector('.clear-compare-btn').addEventListener('click', function() {
                    compareList = [];
                    localStorage.removeItem('compareList');
                    floatingButton.remove();
                    updateCompareButtons();
                    showNotification('Comparison list cleared', 'info');
                });
            } else {
                floatingButton.querySelector('.compare-count').textContent = compareList.length;
            }
        } else if (floatingButton) {
            floatingButton.remove();
        }
    }
}

// ===== Tool Search ===== //
function initToolSearch() {
    const searchInput = document.querySelector('input[name="q"]');
    const searchForm = document.querySelector('.search-input-group').closest('form');
    
    if (searchInput && searchForm) {
        // Add search suggestions (future enhancement)
        searchInput.addEventListener('input', function() {
            const query = this.value.trim();
            if (query.length >= 2) {
                // Could implement live search suggestions here
                console.log('Searching for:', query);
            }
        });
        
        // Handle form submission
        searchForm.addEventListener('submit', function(e) {
            const query = searchInput.value.trim();
            if (!query) {
                e.preventDefault();
                showNotification('Please enter a search term', 'warning');
            }
        });
    }
}

// ===== View Toggle ===== //
function initViewToggle() {
    const viewButtons = document.querySelectorAll('.view-option');
    const toolsGrid = document.querySelector('.tools-grid');
    
    if (!viewButtons.length || !toolsGrid) return;
    
    viewButtons.forEach(button => {
        button.addEventListener('click', function() {
            viewButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            
            const view = this.dataset.view;
            
            if (view === 'list') {
                toolsGrid.style.gridTemplateColumns = '1fr';
                toolsGrid.style.gap = '1rem';
                
                // Modify tool cards for list view
                const toolCards = toolsGrid.querySelectorAll('.tool-card');
                toolCards.forEach(card => {
                    card.style.display = 'flex';
                    card.style.alignItems = 'center';
                    card.style.padding = '1rem';
                    
                    const cardBody = card.querySelector('.tool-card-body');
                    if (cardBody) {
                        cardBody.style.flex = '1';
                        cardBody.style.padding = '0 1rem';
                    }
                    
                    const cardFooter = card.querySelector('.tool-card-footer');
                    if (cardFooter) {
                        cardFooter.style.padding = '0';
                        cardFooter.style.flexDirection = 'row';
                    }
                });
            } else {
                // Grid view
                toolsGrid.style.gridTemplateColumns = 'repeat(auto-fill, minmax(350px, 1fr))';
                toolsGrid.style.gap = '2rem';
                
                // Reset tool cards for grid view
                const toolCards = toolsGrid.querySelectorAll('.tool-card');
                toolCards.forEach(card => {
                    card.style.display = 'block';
                    card.style.padding = '';
                    
                    const cardBody = card.querySelector('.tool-card-body');
                    if (cardBody) {
                        cardBody.style.flex = '';
                        cardBody.style.padding = '';
                    }
                    
                    const cardFooter = card.querySelector('.tool-card-footer');
                    if (cardFooter) {
                        cardFooter.style.padding = '';
                        cardFooter.style.flexDirection = '';
                    }
                });
            }
            
            // Save preference
            localStorage.setItem('toolsViewPreference', view);
        });
    });
    
    // Load saved preference
    const savedView = localStorage.getItem('toolsViewPreference');
    if (savedView) {
        const savedButton = document.querySelector(`[data-view="${savedView}"]`);
        if (savedButton) {
            savedButton.click();
        }
    }
}

// ===== Utility Functions ===== //
function showNotification(message, type = 'success') {
    if (window.TechyVia && window.TechyVia.showNotification) {
        window.TechyVia.showNotification(message, type);
    } else {
        // Fallback notification
        console.log(`${type.toUpperCase()}: ${message}`);
        
        // Create simple notification
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            top: 100px;
            right: 20px;
            background: var(--glass-bg);
            backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border);
            border-radius: 12px;
            padding: 1rem 1.5rem;
            color: var(--text-primary);
            z-index: 10000;
            animation: slideIn 0.3s ease;
        `;
        
        notification.innerHTML = `
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : type === 'warning' ? 'exclamation-triangle' : 'info-circle'}"></i>
                <span>${message}</span>
            </div>
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.remove();
        }, 4000);
    }
}

// ===== Export for global access ===== //
window.TechyVia.AITools = {
    showNotification
};
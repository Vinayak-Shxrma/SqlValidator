document.addEventListener('DOMContentLoaded', () => {
    const validateBtn = document.getElementById('validateBtn');
    const sqlQueryInput = document.getElementById('sqlQuery');
    
    // Output containers
    const tokensContent = document.getElementById('tokensContent');
    const errorsContent = document.getElementById('errorsContent');
    const suggestionsContent = document.getElementById('suggestionsContent');

    validateBtn.addEventListener('click', async () => {
        const query = sqlQueryInput.value.trim();
        
        if (!query) {
            alert('Please enter an SQL query.');
            return;
        }

        // Reset outputs
        tokensContent.innerHTML = 'Analyzing...';
        errorsContent.innerHTML = '';
        suggestionsContent.innerHTML = '';
        
        try {
            const response = await fetch('/validate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ query })
            });
            
            const data = await response.json();
            
            // Render Tokens
            if (data.tokens && data.tokens.length > 0) {
                tokensContent.innerHTML = data.tokens.map(t => 
                    `<span class="token-badge token-${t.type}" title="${t.type}">${t.value}</span>`
                ).join(' ');
            } else {
                tokensContent.innerHTML = 'No tokens generated.';
            }

            // Render Errors
            const allErrors = [
                ...data.lexical_errors,
                ...data.syntax_errors,
                ...data.semantic_errors
            ];
            
            if (allErrors.length > 0) {
                errorsContent.innerHTML = allErrors.map(e => `<div>❌ ${e}</div>`).join('');
            } else {
                errorsContent.innerHTML = '<div style="color: var(--success); font-weight: 600;">✅ Query is perfectly valid!</div>';
            }

            // Render Suggestions
            if (data.suggestions && data.suggestions.length > 0) {
                suggestionsContent.innerHTML = data.suggestions.map(s => `<div>💡 ${s}</div>`).join('');
            } else {
                suggestionsContent.innerHTML = 'No suggestions needed.';
            }

        } catch (error) {
            console.error('Error:', error);
            errorsContent.innerHTML = `<div>❌ System Error: Could not connect to the backend.</div>`;
        }
    });
});

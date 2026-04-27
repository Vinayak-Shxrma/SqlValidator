document.addEventListener('DOMContentLoaded', () => {
    // UI Elements
    const validateBtn = document.getElementById('validateBtn');
    const sqlQueryInput = document.getElementById('sqlQuery');
    const globalStatus = document.getElementById('globalStatus');
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabPanes = document.querySelectorAll('.tab-pane');
    
    // Allow advanced panning and zooming functionality on SVG containers
    document.querySelectorAll('.svg-container').forEach(container => {
        let isDown = false;
        let startX, startY;
        let translateX = 20, translateY = 20, scale = 1;
        
        container.addEventListener('wheel', (e) => {
            e.preventDefault();
            const zoomSensitivity = 0.001;
            const delta = -e.deltaY * zoomSensitivity;
            const newScale = scale * (1 + delta);
            if(newScale > 0.1 && newScale < 5) { scale = newScale; }
            applyTransform();
        });

        container.addEventListener('mousedown', (e) => {
            isDown = true; container.style.cursor = 'grabbing';
            startX = e.pageX - translateX; startY = e.pageY - translateY;
        });
        container.addEventListener('mouseleave', () => { isDown = false; container.style.cursor = 'default'; });
        container.addEventListener('mouseup', () => { isDown = false; container.style.cursor = 'default'; });
        container.addEventListener('mousemove', (e) => {
            if (!isDown) return; e.preventDefault();
            translateX = e.pageX - startX; translateY = e.pageY - startY;
            applyTransform();
        });

        function applyTransform() {
            const svgG = container.querySelector('svg > g');
            if (svgG) svgG.setAttribute('transform', `translate(${translateX}, ${translateY}) scale(${scale})`);
        }
        
        // Reset transform on content change
        const observer = new MutationObserver(() => {
            translateX = 20; translateY = 20; scale = 1; applyTransform();
        });
        observer.observe(container, { childList: true });
    });

    // Tab switching logic
    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            tabBtns.forEach(b => b.classList.remove('active'));
            tabPanes.forEach(p => p.classList.remove('active'));
            btn.classList.add('active');
            document.getElementById(btn.dataset.target).classList.add('active');
        });
    });

    // Output containers
    const lexicalContent = document.getElementById('lexicalContent');
    const lexicalErrors = document.getElementById('lexicalErrors');
    const astSvgContainer = document.getElementById('astSvgContainer');
    const astErrors = document.getElementById('astErrors');
    const aiSuggestions = document.getElementById('aiSuggestions');

    function drawSVGTree(containerId, treeData) {
        if (!treeData || Object.keys(treeData).length === 0) {
            document.getElementById(containerId).innerHTML = '<p class="text-muted text-center mt-4">No tree to render.</p>';
            return;
        }

        function convertAST(node, key = "Query") {
            let result = { name: String(key) };
            if (typeof node !== 'object' || node === null) {
                result.children = [{ name: String(node), type: "leaf", children: null }];
                result.type = "child";
            } else if (Array.isArray(node)) {
                result.children = node.map((n, i) => {
                    if (typeof n !== 'object' || n === null) {
                        return { name: String(n), type: "leaf", children: null };
                    }
                    return convertAST(n, `Item ${i}`);
                });
                result.type = "child";
            } else {
                result.children = [];
                if (node.type) { result.name = node.type; }
                for (let k in node) {
                    if (k === 'type') continue;
                    let child = convertAST(node[k], k);
                    result.children.push(child);
                }
                result.type = "child";
            }
            return result;
        }

        let rootStruct = convertAST(treeData, "QUERY");
        let rectWidth = 160, rectHeight = 40, gapX = 40, gapY = 80;
        
        function layoutTree(node, depth = 0, baseX = 0) {
            node.y = depth * gapY;
            if (!node.children || node.children.length === 0) {
                node.x = baseX;
                return baseX + rectWidth + gapX;
            }
            let nextX = baseX;
            node.children.forEach(child => {
                nextX = layoutTree(child, depth + 1, nextX);
            });
            node.x = (node.children[0].x + node.children[node.children.length - 1].x) / 2;
            return nextX;
        }
        
        layoutTree(rootStruct);
        
        function getSVGContent(node, depth) {
            let svgStr = "";
            let cssClass = depth === 0 ? "root" : (node.type === "leaf" ? "leaf" : "child");
            
            if (node.children) {
                node.children.forEach(child => {
                    svgStr += `<path class="link" d="M${node.x + rectWidth/2},${node.y + rectHeight} C${node.x + rectWidth/2},${node.y + rectHeight + gapY/2} ${child.x + rectWidth/2},${child.y - gapY/2} ${child.x + rectWidth/2},${child.y}" />`;
                    svgStr += getSVGContent(child, depth + 1);
                });
            }
            
            svgStr += `<g class="node ${cssClass}" transform="translate(${node.x},${node.y})">
                            <rect width="${rectWidth}" height="${rectHeight}"></rect>
                            <text x="${rectWidth/2}" y="${rectHeight/2}">${node.name}</text>
                        </g>`;
            return svgStr;
        }
        
        let maxX = layoutTree(rootStruct) - gapX;
        let maxY = (function getMaxDepth(n, d) { return n.children ? Math.max(...n.children.map(c=>getMaxDepth(c,d+1))) : d; })(rootStruct, 0) * gapY + rectHeight;
        
        let svgHtml = `<svg width="100%" height="100%" style="overflow: visible;">
            <g transform="translate(20, 20) scale(1)">
                ${getSVGContent(rootStruct, 0)}
            </g>
        </svg>`;
        
        document.getElementById(containerId).innerHTML = svgHtml;
    }

    validateBtn.addEventListener('click', async () => {
        const query = sqlQueryInput.value.trim();
        if (!query) return alert('Please enter an SQL query.');

        validateBtn.disabled = true;
        validateBtn.innerHTML = '<i data-feather="loader" class="feather-pulse"></i> Analyzing...';
        feather.replace();

        globalStatus.className = 'global-status hidden';

        try {
            const response = await fetch('/validate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query })
            });
            const data = await response.json();

            const lexErrs = data.lexical_errors || [];
            const synErrs = data.syntax_errors || [];
            const semErrs = data.semantic_errors || [];
            const allErrors = lexErrs.concat(synErrs).concat(semErrs);

            // Render Lexical Tab
            lexicalErrors.innerHTML = (data.lexical_errors || []).map(e => `<div class="error-alert"><i data-feather="alert-circle"></i>${e}</div>`).join('');
            if (data.tokens && data.tokens.length > 0) {
                const grouped = data.tokens.reduce((acc, t) => {
                    let type = t.type || t[0]; let val = t.value || t[1];
                    if (!acc[type]) acc[type] = [];
                    acc[type].push(val);
                    return acc;
                }, {});
                
                lexicalContent.innerHTML = Object.entries(grouped).map(([type, tokens]) => `
                    <div class="token-category">
                        <div class="token-category-header">
                            <span>${type}</span>
                            <span class="text-muted">${tokens.length}</span>
                        </div>
                        <div class="token-list">
                            ${tokens.map(tk => `<span class="token-badge token-${type}">${tk}</span>`).join('')}
                        </div>
                    </div>
                `).join('');
            } else {
                lexicalContent.innerHTML = '<p class="text-muted text-center mt-4">No tokens extracted.</p>';
            }

            // Combine Errors for AST Display
            let errorHtml = "";
            if (lexErrs.length > 0) errorHtml += lexErrs.map(e => `<div class="error-alert"><i data-feather="alert-circle"></i>${e}</div>`).join('');
            if (synErrs.length > 0) errorHtml += synErrs.map(e => `<div class="error-alert"><i data-feather="alert-triangle"></i>${e}</div>`).join('');
            if (semErrs.length > 0) errorHtml += semErrs.map(e => `<div class="error-alert"><i data-feather="x-square"></i>${e}</div>`).join('');
            
            astErrors.innerHTML = errorHtml;

            if (allErrors.length > 0) {
                // Do not render AST when errors exist
                astSvgContainer.innerHTML = '<p class="text-error text-center mt-4">Invalid Query. Check errors above. AST not generated.</p>';
                globalStatus.innerText = `Compilation Failed with ${allErrors.length} errors.`;
                globalStatus.className = 'global-status error';
            } else {
                drawSVGTree('astSvgContainer', data.ast);
                globalStatus.innerHTML = '<i data-feather="check-circle"></i> Query validated successfully without any errors.';
                globalStatus.className = 'global-status success';
            }

            if (data.suggestions && data.suggestions.length > 0) {
                aiSuggestions.innerHTML = data.suggestions.map(s => `<div class="ai-suggestion-item"><i data-feather="message-circle" class="text-warning"></i><span>${s}</span></div>`).join('');
            } else {
                aiSuggestions.innerHTML = `<p class="text-muted text-center mt-4"><i data-feather="thumbs-up" class="text-success"></i> Code is optimal. No AI suggestions needed.</p>`;
            }

        } catch (error) {
            console.error(error);
            globalStatus.innerText = 'Failed to communicate with backend.';
            globalStatus.className = 'global-status error';
        }

        validateBtn.disabled = false;
        validateBtn.innerHTML = '<i data-feather="play"></i> Analyze Query';
        feather.replace();
    });
});

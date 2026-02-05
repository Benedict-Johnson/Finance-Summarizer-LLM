document.getElementById('queryBtn').addEventListener('click', fetchData);
document.getElementById('entityInput').addEventListener('keyup', (event) => {
    if (event.key === "Enter") fetchData();
});

async function fetchData() {
    const userPrompt = document.getElementById('entityInput').value;
    const summaryOutput = document.getElementById('summary-output');
    const graphContainer = document.getElementById('graph-container');
    
    if (!userPrompt) {
        alert("Please enter a question to analyze.");
        return;
    }

    summaryOutput.innerHTML = '<pre class="placeholder-text">🤖 AI is thinking...</pre>';
    graphContainer.innerHTML = '<span class="placeholder-text">Loading graph...</span>';

    try {
        const response = await fetch(`http://127.0.0.1:5000/query?q=${encodeURIComponent(userPrompt)}`);
        const data = await response.json();
        
        if (data.error) {
            summaryOutput.innerHTML = `<pre>Error: ${data.error}</pre>`;
            return;
        }

        summaryOutput.innerHTML = `<pre>${data.summary}</pre>`;
        if (data.edges.length > 0) {
            drawGraph(data.edges);
        } else {
            graphContainer.innerHTML = '<span class="placeholder-text">No graph to display.</span>';
        }

    } catch (error) {
        summaryOutput.innerHTML = '<pre>❌ Failed to connect to the backend server. Is it running?</pre>';
        console.error("Fetch error:", error);
    }
}

function drawGraph(relations) {
    const container = document.getElementById('graph-container');
    const nodes = new vis.DataSet();
    const edges = new vis.DataSet();
    const uniqueNodes = new Set();
    
    relations.forEach(([sub, obj, rel]) => {
        uniqueNodes.add(sub);
        uniqueNodes.add(obj);
        edges.add({ from: sub, to: obj, label: rel, arrows: 'to', font: { align: 'middle', color: '#555', strokeWidth: 0 } });
    });

    uniqueNodes.forEach(node => {
        nodes.add({ id: node, label: node });
    });

    const data = { nodes, edges };
    const options = {
        nodes: { shape: 'box', color: { background: '#D2E5FF', border: '#2B7CE9' }, font: { color: '#343434' } },
        edges: { color: '#848484', smooth: { type: 'dynamic' } },
        physics: { stabilization: { iterations: 150 } },
        layout: { improvedLayout: true }
    };
    
    new vis.Network(container, data, options);
}
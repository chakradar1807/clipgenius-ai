async function generate() {
    const url = document.getElementById("url").value;
    document.getElementById("status").innerText = "Processing with AI... ⏳";

    const res = await fetch("http://127.0.0.1:8000/generate-ai-reels", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({url})
    });

    const data = await res.json();

    if (data.status === "success") {
        document.getElementById("status").innerText = "✅ Done";

        let html = "<h3>Generated Clips:</h3>";
        data.clips.forEach((clip, i) => {
            html += `<a href="http://127.0.0.1:8000/download?file=${clip}" target="_blank">Download Clip ${i+1}</a><br/>`;
        });

        html += `<h3>AI Analysis:</h3><pre>${data.ai_analysis}</pre>`;

        document.getElementById("results").innerHTML = html;
    } else {
        document.getElementById("status").innerText = "❌ Error";
    }
}
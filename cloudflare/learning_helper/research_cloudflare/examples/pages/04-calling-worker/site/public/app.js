// Set this to the Worker URL for the direct browser call.
// Local dev:    "http://localhost:8789"
// Deployed:     "https://calling-worker-api.<your-subdomain>.workers.dev"
// Leave empty to skip the direct call.
const WORKER_URL = "https://calling-worker-api.jefferson-soto.workers.dev/";

async function call(path, body) {
	const res = await fetch(path, {
		method: "POST",
		headers: { "content-type": "application/json" },
		body: JSON.stringify(body),
	});
	const text = await res.text();
	try {
		return JSON.stringify(JSON.parse(text), null, 2);
	} catch {
		return text;
	}
}

document.getElementById("callBrowser").addEventListener("click", async () => {
	const out = document.getElementById("outBrowser");
	if (!WORKER_URL) {
		out.textContent =
			"WORKER_URL is empty in app.js. Edit the file and set it to your Worker URL.";
		return;
	}
	out.textContent = "Calling...";
	out.textContent = await call(WORKER_URL + "/echo", { hello: "browser" });
});

document.getElementById("callBinding").addEventListener("click", async () => {
	const out = document.getElementById("outBinding");
	out.textContent = "Calling...";
	out.textContent = await call("/api/via-binding", { hello: "binding" });
});

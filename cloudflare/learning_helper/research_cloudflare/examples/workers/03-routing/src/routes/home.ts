export function home() {
	return new Response("Home page. Try /about, /api/time, or /api/users/42", {
		headers: { "content-type": "text/plain; charset=utf-8" },
	});
}

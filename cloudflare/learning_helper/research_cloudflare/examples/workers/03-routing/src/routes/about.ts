export function about() {
	return new Response("About page. Routing keeps handlers tidy.", {
		headers: { "content-type": "text/plain; charset=utf-8" },
	});
}

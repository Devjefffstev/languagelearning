/**
 * 02 - Request / Response
 *
 * Workers receive a web-standard `Request` and must return a `Response`.
 * This example inspects the request (method, URL, headers, body) and
 * demonstrates a few common response patterns.
 */

function jsonResponse(data: unknown, status = 200): Response {
	return new Response(JSON.stringify(data, null, 2), {
		status,
		headers: { "content-type": "application/json; charset=utf-8" },
	});
}

export default {
	async fetch(request: Request): Promise<Response> {
		const { method } = request;
		const url = new URL(request.url);

		if (method === "GET" && url.pathname === "/") {
			return new Response(
				`Try: /echo, /headers, /upper?text=hello, /upper (POST body: hello)`,
				{ headers: { "content-type": "text/plain; charset=utf-8" } },
			);
		}

		if (url.pathname === "/echo") {
			return jsonResponse({
				method,
				pathname: url.pathname,
				query: Object.fromEntries(url.searchParams),
				headers: Object.fromEntries(request.headers),
			});
		}

		if (url.pathname === "/headers") {
			return jsonResponse({
				userAgent: request.headers.get("user-agent"),
				country: request.cf?.country,
				colo: request.cf?.colo,
			});
		}

		if (url.pathname === "/upper") {
			let text = url.searchParams.get("text") ?? "";
			if (!text && method === "POST") {
				text = await request.text();
			}
			return new Response(text.toUpperCase(), {
				headers: { "content-type": "text/plain; charset=utf-8" },
			});
		}

		return new Response("Not Found", { status: 404 });
	},
};

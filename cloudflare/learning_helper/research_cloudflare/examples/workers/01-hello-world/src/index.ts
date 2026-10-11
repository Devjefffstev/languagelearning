/**
 * 01 - Hello World
 *
 * The smallest possible Worker. Every Worker exports an object with a
 * `fetch` handler. Cloudflare hands it a Request and expects a Response back.
 */

export default {
	async fetch(_request: Request): Promise<Response> {
		return new Response("Hello from a Cloudflare Worker!", {
			headers: { "content-type": "text/plain; charset=utf-8" },
		});
	},
};

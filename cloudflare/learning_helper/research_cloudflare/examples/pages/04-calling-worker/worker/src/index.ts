/**
 * The "backend" Worker. It accepts POST /echo with a JSON body and
 * returns the payload plus a server-side timestamp and identifier.
 *
 * Called either:
 *   - directly from the browser (Worker needs a public URL), or
 *   - from a Pages Function over a service binding (no public URL needed).
 */

interface Env {
	API_NAME: string;
}

export default {
	async fetch(request: Request, env: Env): Promise<Response> {
		const url = new URL(request.url);

		if (url.pathname === "/echo" && request.method === "POST") {
			const payload = await request.json().catch(() => ({}));
			return Response.json({
				receivedAt: new Date().toISOString(),
				worker: env.API_NAME,
				caller: request.headers.get("x-caller") ?? "unknown",
				tokenPresent: Boolean(request.headers.get("x-internal-token")),
				payload,
			});
		}

		return new Response('Send POST {"foo":"bar"} to /echo', {
			headers: { "content-type": "text/plain; charset=utf-8" },
		});
	},
};

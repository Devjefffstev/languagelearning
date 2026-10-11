/**
 * 05 - Cloudflare KV
 *
 * KV is a low-latency, eventually-consistent key/value store.
 * Reads are fast and globally cached; writes propagate within ~60s.
 * Perfect for counters, sessions, feature flags, config snapshots.
 *
 *   GET    /            -> show current count
 *   POST   /            -> increment
 *   DELETE /            -> reset to 0
 *
 * Wrangler wires the namespace as `env.COUNTERS` (see wrangler.jsonc).
 */

interface Env {
	COUNTERS: KVNamespace;
}

export default {
	async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
		const key = "hits";
		const url = new URL(request.url);

		if (request.method === "POST") {
			const current = Number((await env.COUNTERS.get(key)) ?? "0");
			const next = current + 1;
			await env.COUNTERS.put(key, String(next));
			return Response.json({ count: next });
		}

		if (request.method === "DELETE") {
			await env.COUNTERS.delete(key);
			return Response.json({ count: 0, reset: true });
		}

		const stored = await env.COUNTERS.get(key);
		const count = Number(stored ?? "0");

		// ctx.waitUntil lets you keep working after the response is sent.
		// For demos we just count this same request too.
		ctx.waitUntil(env.COUNTERS.put(key, String(count + 1)));

		return new Response(
			`<p>Visits: <strong>${count + 1}</strong></p>
			 <form method="POST"><button>Increment now</button></form>
			 <form method="POST" action="/?reset" onsubmit="event.preventDefault();fetch('/',{method:'DELETE'}).then(()=>location.reload())">
			   <button type="submit">Reset</button>
			 </form>`,
			{ headers: { "content-type": "text/html; charset=utf-8" } },
		);
	},
};

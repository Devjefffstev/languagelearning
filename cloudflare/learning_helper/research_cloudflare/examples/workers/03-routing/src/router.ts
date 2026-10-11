/**
 * Tiny router. For real apps use itty-router, Hono, or Workers-Router.
 * Kept inline here so the example stays readable.
 */

type Handler = (params: Record<string, string>, request: Request) => Promise<Response> | Response;

interface Route {
	method: string;
	pattern: string;
	handler: Handler;
}

function compile(pattern: string): RegExp {
	const keys: string[] = [];
	const regex = pattern
		.replace(/\//g, "\\/")
		.replace(/:(\w+)/g, (_, key) => {
			keys.push(key);
			return "([^/]+)";
		});
	return new RegExp(`^${regex}$`);
}

export function router(request: Request, routes: Route[]): Response {
	const url = new URL(request.url);
	for (const route of routes) {
		if (route.method !== request.method) continue;
		const re = compile(route.pattern);
		const match = url.pathname.match(re);
		if (!match) continue;

		const params: Record<string, string> = {};
		const keys = (route.pattern.match(/:(\w+)/g) ?? []).map((k) => k.slice(1));
		keys.forEach((k, i) => (params[k] = decodeURIComponent(match[i + 1])));

		return route.handler(params, request);
	}

	return new Response("Not Found", { status: 404 });
}

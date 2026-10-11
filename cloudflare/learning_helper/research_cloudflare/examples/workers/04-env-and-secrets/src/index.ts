/**
 * 04 - Env vars & secrets
 *
 * - `vars` in wrangler.jsonc  -> non-sensitive config, committed to git.
 * - `.dev.vars`                -> local-only env file (gitignored).
 * - `wrangler secret put NAME` -> encrypted secret stored on Cloudflare.
 *
 * Both end up on `env` (the second argument to fetch).
 */

interface Env {
	GREETING: string;
	ENVIRONMENT: string;
	API_KEY?: string;
}

function mask(value: string | undefined): string {
	if (!value) return "<unset>";
	if (value.length <= 4) return "****";
	return `${value.slice(0, 2)}***${value.slice(-2)} (len=${value.length})`;
}

export default {
	async fetch(request: Request, env: Env): Promise<Response> {
		const name = new URL(request.url).searchParams.get("name") ?? "world";

		return Response.json({
			message: `${env.GREETING}, ${name}!`,
			environment: env.ENVIRONMENT,
			apiKey: mask(env.API_KEY),
		});
	},
};

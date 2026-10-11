/**
 * Calls the bound Worker. This Function:
 *   - never exposes the Worker's URL to the browser,
 *   - reads INTERNAL_TOKEN from env (server-side only),
 *   - forwards the request to the Worker in-process over the service binding.
 *
 * The URL passed to env.API.fetch is opaque — it is parsed but not actually
 * fetched from the network.
 */

interface Env {
	API: Fetcher;
	INTERNAL_TOKEN: string;
}

export const onRequestPost: PagesFunction<unknown, Env> = async ({ request, env }) => {
	const payload = await request.json().catch(() => ({}));

	const workerRequest = new Request("https://internal/echo", {
		method: "POST",
		headers: {
			"content-type": "application/json",
			"x-internal-token": env.INTERNAL_TOKEN,
			"x-caller": "pages-function",
		},
		body: JSON.stringify(payload),
	});

	const workerResponse = await env.API.fetch(workerRequest);
	const workerBody = await workerResponse.json();

	return Response.json({
		via: "service-binding",
		calledAt: new Date().toISOString(),
		workerResponse: workerBody,
	});
};

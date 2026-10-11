interface Env {
	API: Fetcher;
	INTERNAL_TOKEN: string;
}

export const onRequestPost: PagesFunction<unknown, Env> = async ({ request, env }) => {
	// TODO: build a Request that targets the Worker (e.g. POST https://internal/ping)
	// with the JSON body and an x-internal-token header from env.INTERNAL_TOKEN.
	// Call env.API.fetch(<that request>), parse the JSON, and return:
	// { via: "service-binding", worker: <worker-json> }
	return new Response("Not implemented", { status: 501 });
};

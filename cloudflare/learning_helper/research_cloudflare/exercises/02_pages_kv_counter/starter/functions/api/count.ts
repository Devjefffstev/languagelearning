interface Env {
	COUNTERS: KVNamespace;
}

export const onRequestGet: PagesFunction<unknown, Env> = async ({ env }) => {
	// TODO: read the counter from env.COUNTERS (key "hits"), default to 0 if missing,
	// return Response.json({ count: <number> }).
	return new Response("Not implemented", { status: 501 });
};

export const onRequestPost: PagesFunction<unknown, Env> = async ({ env }) => {
	// TODO: read the counter, increment by 1, write it back, and return
	// Response.json({ count: <new number> }).
	return new Response("Not implemented", { status: 501 });
};

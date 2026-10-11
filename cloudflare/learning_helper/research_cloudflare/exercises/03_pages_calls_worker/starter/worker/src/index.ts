/**
 * Exercise 03 — Worker side.
 *
 * Accept POST /ping with a JSON body and return
 * { pong: true, receivedAt: <iso>, payload: <body> }.
 */
export default {
	async fetch(request: Request): Promise<Response> {
		// TODO: if request.method === "POST" and url.pathname === "/ping",
		// read JSON body and return Response.json({ pong: true, receivedAt: new Date().toISOString(), payload }).
		// Otherwise return a 200 plain text hint.
		return new Response("Not implemented", { status: 501 });
	},
};

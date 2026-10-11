/**
 * 03 - Routing
 *
 * A Worker is one function. For real apps you split routes across files.
 * This example shows a tiny router + per-route handler modules.
 */

import { router } from "./router";
import { home } from "./routes/home";
import { about } from "./routes/about";
import { time } from "./routes/time";
import { user } from "./routes/user";

export default {
	async fetch(request: Request): Promise<Response> {
		return router(request, [
			{ method: "GET", pattern: "/", handler: home },
			{ method: "GET", pattern: "/about", handler: about },
			{ method: "GET", pattern: "/api/time", handler: time },
			{ method: "GET", pattern: "/api/users/:id", handler: user },
		]);
	},
};

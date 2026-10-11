/**
 * Pages Functions live in `functions/` and are auto-routed by filename.
 * `functions/api/hello.ts` -> handles GET/POST/etc. for `/api/hello`.
 *
 * Each function exports handlers named `onRequestGet`, `onRequestPost`, ...
 * or a single `onRequest` for any method.
 */

export const onRequestGet: PagesFunction = async () => {
	return Response.json({
		message: "Hello from a Pages Function!",
		note: "Pages Functions are Workers under the hood.",
	});
};
